#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::io;
use std::net::TcpStream;
use std::os::windows::process::CommandExt;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

const CREATE_NO_WINDOW: u32 = 0x08000000;

fn kill_process_on_port(port: u16) {
    let output = Command::new("netstat")
        .args(["-ano"])
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .output();
    if let Ok(output) = output {
        let stdout = String::from_utf8_lossy(&output.stdout);
        for line in stdout.lines() {
            let line = line.trim();
            if line.contains(&format!(":{}", port)) {
                let parts: Vec<&str> = line.split_whitespace().collect();
                if let Some(pid_str) = parts.last() {
                    if let Ok(pid) = pid_str.parse::<u32>() {
                        if pid > 0 {
                            let _ = Command::new("taskkill")
                                .args(["/F", "/PID", &pid.to_string()])
                                .stdout(Stdio::null())
                                .stderr(Stdio::null())
                                .spawn();
                        }
                    }
                }
            }
        }
    }
}

fn is_backend_running() -> bool {
    TcpStream::connect("127.0.0.1:8000").is_ok()
}

fn install_python_app_candidates() -> Vec<PathBuf> {
    let mut candidates = Vec::new();
    if let Ok(exe) = std::env::current_exe() {
        if let Some(exe_dir) = exe.parent() {
            // MSI/NSIS installation structure
            candidates.push(exe_dir.join("_up_").join("python_app"));
            candidates.push(exe_dir.join("resources").join("python_app"));
            candidates.push(exe_dir.join("python_app"));
        }
    }
    candidates
}

fn resolve_python_app(path_resolver: tauri::PathResolver) -> io::Result<PathBuf> {
    let log_path = std::env::temp_dir().join("biblical_study_launcher_rust.log");
    let mut log_content = String::new();

    // 1. Installed executable dir candidates
    for candidate in install_python_app_candidates() {
        log_content.push_str(&format!("Checking candidate: {:?}\n", candidate));
        if candidate.exists() {
            log_content.push_str(&format!("Found: {:?}\n", candidate));
            let _ = std::fs::write(&log_path, log_content);
            return Ok(candidate);
        }
    }

    // 2. Resource dir (production resources)
    if let Some(resource_dir) = path_resolver.resource_dir() {
        let candidate = resource_dir.join("python_app");
        log_content.push_str(&format!("Checking resource_dir: {:?}\n", candidate));
        if candidate.exists() {
            log_content.push_str(&format!("Found: {:?}\n", candidate));
            let _ = std::fs::write(&log_path, log_content);
            return Ok(candidate);
        }
    }

    // 3. App data fallback (updater/runtime extracted location)
    if let Some(app_data) = path_resolver.app_data_dir() {
        let candidate = app_data.join("python_app");
        log_content.push_str(&format!("Checking app_data: {:?}\n", candidate));
        if candidate.exists() {
            log_content.push_str(&format!("Found: {:?}\n", candidate));
            let _ = std::fs::write(&log_path, log_content);
            return Ok(candidate);
        }
    }

    // 4. Dev fallback (source tree)
    let dev_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("python_app");
    log_content.push_str(&format!("Checking dev_path: {:?}\n", dev_path));
    if dev_path.exists() {
        log_content.push_str(&format!("Found: {:?}\n", dev_path));
        let _ = std::fs::write(&log_path, log_content);
        return Ok(dev_path);
    }

    let err = format!("python_app directory not found. Log: {}", log_content);
    let _ = std::fs::write(&log_path, &err);
    Err(io::Error::new(io::ErrorKind::NotFound, err))
}

#[cfg(target_os = "windows")]
fn start_backend(workdir: &Path) -> io::Result<()> {
    Command::new("cmd")
        .args(["/C", "call", "start_api.bat"])
        .current_dir(workdir)
        .creation_flags(CREATE_NO_WINDOW)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()?;
    Ok(())
}

#[cfg(any(target_os = "linux", target_os = "macos"))]
fn start_backend(workdir: &Path) -> io::Result<()> {
    Command::new("sh")
        .arg("start_api.sh")
        .current_dir(workdir)
        .spawn()?;
    Ok(())
}

#[tauri::command]
fn read_log() -> Result<String, String> {
    let log_path = std::env::temp_dir().join("biblical_study_api.log");
    match std::fs::read_to_string(&log_path) {
        Ok(content) => Ok(content),
        Err(err) => Err(format!("cannot read log {}: {}", log_path.display(), err)),
    }
}

#[tauri::command]
fn ensure_backend_started(app: tauri::AppHandle) -> Result<bool, String> {
    if is_backend_running() {
        return Ok(false);
    }
    let workdir = resolve_python_app(app.path_resolver()).map_err(|e| e.to_string())?;
    start_backend(&workdir).map_err(|e| e.to_string())?;
    Ok(true)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![read_log, ensure_backend_started])
        .setup(|app| {
            // Kill any stale backend process to ensure a fresh start
            kill_process_on_port(8000);
            std::thread::sleep(std::time::Duration::from_secs(1));
            // Start fresh backend
            let workdir = resolve_python_app(app.path_resolver())?;
            start_backend(&workdir)?;
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
