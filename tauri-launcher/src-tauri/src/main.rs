#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::io::{self, Write};
use std::net::TcpStream;
use std::os::windows::process::CommandExt;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Duration;
use std::{fs, thread};

use serde::Serialize;

const CREATE_NO_WINDOW: u32 = 0x08000000;

// ---------------------------------------------------------------------------
// Shared backend state, accessible from Tauri commands and the monitor thread
// ---------------------------------------------------------------------------
struct BackendState {
    running: AtomicBool,
    pid: Mutex<Option<u32>>,
    last_error: Mutex<String>,
}

#[derive(Clone, Serialize)]
struct BackendStatus {
    running: bool,
    pid: Option<u32>,
    last_error: String,
}

// ---------------------------------------------------------------------------
// Port helpers
// ---------------------------------------------------------------------------

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
                if let Some(pid_str) = line.split_whitespace().last() {
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

fn wait_for_backend(timeout_secs: u64) -> bool {
    let start = std::time::Instant::now();
    while start.elapsed().as_secs() < timeout_secs {
        if is_backend_running() {
            return true;
        }
        thread::sleep(Duration::from_millis(500));
    }
    false
}

// ---------------------------------------------------------------------------
// Python-app directory resolution (unchanged logic)
// ---------------------------------------------------------------------------

fn install_python_app_candidates() -> Vec<PathBuf> {
    let mut candidates = Vec::new();
    if let Ok(exe) = std::env::current_exe() {
        if let Some(exe_dir) = exe.parent() {
            candidates.push(exe_dir.join("_up_").join("python_app"));
            candidates.push(exe_dir.join("python_app"));
            candidates.push(exe_dir.join("resources").join("python_app"));
            if let Some(parent) = exe_dir.parent() {
                if let Some(grandparent) = parent.parent() {
                    candidates.push(grandparent.join("python_app"));
                }
            }
        }
    }
    candidates
}

fn resolve_python_app(path_resolver: tauri::PathResolver) -> io::Result<PathBuf> {
    let log_path = std::env::temp_dir().join("biblical_study_launcher_rust.log");
    let mut log_content = String::new();

    for candidate in install_python_app_candidates() {
        log_content.push_str(&format!("Checking candidate: {:?}\n", candidate));
        if candidate.exists() {
            log_content.push_str(&format!("Found: {:?}\n", candidate));
            let _ = fs::write(&log_path, &log_content);
            return Ok(candidate);
        }
    }

    if let Some(resource_dir) = path_resolver.resource_dir() {
        let candidate = resource_dir.join("python_app");
        log_content.push_str(&format!("Checking resource_dir: {:?}\n", candidate));
        if candidate.exists() {
            let _ = fs::write(&log_path, &log_content);
            return Ok(candidate);
        }
    }

    if let Some(app_data) = path_resolver.app_data_dir() {
        let candidate = app_data.join("python_app");
        log_content.push_str(&format!("Checking app_data: {:?}\n", candidate));
        if candidate.exists() {
            let _ = fs::write(&log_path, &log_content);
            return Ok(candidate);
        }
    }

    let dev_path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("python_app");
    log_content.push_str(&format!("Checking dev_path: {:?}\n", dev_path));
    if dev_path.exists() {
        let _ = fs::write(&log_path, &log_content);
        return Ok(dev_path);
    }

    let err = format!("python_app directory not found. Log: {}", log_content);
    let _ = fs::write(&log_path, &err);
    Err(io::Error::new(io::ErrorKind::NotFound, err))
}

// ---------------------------------------------------------------------------
// Python interpreter resolution
// ---------------------------------------------------------------------------

fn find_python(workdir: &Path) -> PathBuf {
    let py_short = workdir.join("py").join("python.exe");
    if py_short.exists() {
        return py_short;
    }
    let portable = workdir.join("portable_python").join("python.exe");
    if portable.exists() {
        return portable;
    }
    let venv = workdir.join(".venv").join("Scripts").join("python.exe");
    if venv.exists() {
        return venv;
    }
    PathBuf::from("python")
}

// ---------------------------------------------------------------------------
// Backend lifecycle
// ---------------------------------------------------------------------------

fn append_log(msg: &str) {
    let log_path = std::env::temp_dir().join("biblical_study_api_rust.log");
    if let Ok(mut f) = fs::OpenOptions::new().create(true).append(true).open(&log_path)
    {
        let _ = writeln!(f, "[{}] {}", chrono_line(), msg);
    }
}

fn chrono_line() -> String {
    use std::time::{SystemTime, UNIX_EPOCH};
    let d = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default();
    format!("+{:.3}s", d.as_secs_f64())
}

fn start_backend(workdir: &Path, state: &BackendState) -> io::Result<()> {
    let py_exe = find_python(workdir);

    append_log(&format!(
        "Starting backend with: {}",
        py_exe.display()
    ));

    let bundled = workdir.join("bundled_packages");
    let portable_site = workdir.join("py").join("Lib").join("site-packages");
    let portable_site_fallback = workdir.join("portable_python").join("Lib").join("site-packages");

    let mut python_path = workdir.to_string_lossy().to_string();

    if bundled.exists() {
        python_path = format!("{};{}", bundled.display(), python_path);
    }
    if portable_site.exists() {
        python_path = format!("{};{}", portable_site.display(), python_path);
    } else if portable_site_fallback.exists() {
        python_path = format!("{};{}", portable_site_fallback.display(), python_path);
    }

    let env_python_path = format!(
        "{};{}",
        python_path,
        std::env::var("PYTHONPATH").unwrap_or_default()
    );

    append_log(&format!("PYTHONPATH: {}", env_python_path));

    let log_path = std::env::temp_dir().join("biblical_study_api_rust.log");
    let log_file = fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(&log_path)?;

    let child = Command::new(&py_exe)
        .args([
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ])
        .current_dir(workdir)
        .env("PYTHONPATH", &env_python_path)
        .env("PYTHONUNBUFFERED", "1")
        .creation_flags(CREATE_NO_WINDOW)
        .stdin(Stdio::null())
        .stdout(Stdio::from(log_file.try_clone()?))
        .stderr(Stdio::from(log_file))
        .spawn()?;

    *state.pid.lock().unwrap() = Some(child.id());
    append_log(&format!("Backend spawned with PID {}", child.id()));

    Ok(())
}

// ---------------------------------------------------------------------------
// Background monitor — periodically checks health, auto-restarts on failure
// ---------------------------------------------------------------------------

fn start_monitor(workdir: PathBuf, state: Arc<BackendState>) {
    thread::spawn(move || {
        let mut down_count: u32 = 0;
        loop {
            thread::sleep(Duration::from_secs(10));

            if is_backend_running() {
                state.running.store(true, Ordering::SeqCst);
                down_count = 0;
                continue;
            }

            down_count += 1;
            state.running.store(false, Ordering::SeqCst);

            // Only act after 3 consecutive failures (~30s of downtime)
            if down_count < 3 {
                continue;
            }

            down_count = 0;
            let msg = "Backend unreachable for 30s. Attempting auto-restart...";
            append_log(msg);
            *state.last_error.lock().unwrap() = msg.to_string();

            kill_process_on_port(8000);
            thread::sleep(Duration::from_secs(2));

            if let Err(e) = start_backend(&workdir, &state) {
                let err = format!("Auto-restart failed: {}", e);
                append_log(&err);
                *state.last_error.lock().unwrap() = err;
            } else if wait_for_backend(15) {
                state.running.store(true, Ordering::SeqCst);
                append_log("Auto-restart succeeded.");
            } else {
                let err = "Auto-restart: backend started but health check failed".to_string();
                append_log(&err);
                *state.last_error.lock().unwrap() = err;
            }
        }
    });
}

// ---------------------------------------------------------------------------
// Tauri commands
// ---------------------------------------------------------------------------

#[tauri::command]
fn get_backend_status(state: tauri::State<'_, Arc<BackendState>>) -> BackendStatus {
    BackendStatus {
        running: state.running.load(Ordering::SeqCst) && is_backend_running(),
        pid: *state.pid.lock().unwrap(),
        last_error: state.last_error.lock().unwrap().clone(),
    }
}

#[tauri::command]
fn restart_backend(
    app: tauri::AppHandle,
    state: tauri::State<'_, Arc<BackendState>>,
) -> Result<bool, String> {
    append_log("Manual restart requested via IPC.");
    kill_process_on_port(8000);
    thread::sleep(Duration::from_secs(1));

    let workdir =
        resolve_python_app(app.path_resolver()).map_err(|e| format!("resolve: {}", e))?;
    start_backend(&workdir, state.inner()).map_err(|e| format!("start: {}", e))?;

    let ok = wait_for_backend(20);
    state.running.store(ok, Ordering::SeqCst);
    if ok {
        append_log("Manual restart succeeded.");
    } else {
        append_log("Manual restart: health check failed.");
    }
    Ok(ok)
}

#[tauri::command]
fn read_log() -> Result<String, String> {
    let log_path = std::env::temp_dir().join("biblical_study_api_rust.log");
    fs::read_to_string(&log_path).map_err(|e| format!("Cannot read log: {}", e))
}

// ---------------------------------------------------------------------------
// Entrypoint
// ---------------------------------------------------------------------------

fn main() {
    let state = Arc::new(BackendState {
        running: AtomicBool::new(false),
        pid: Mutex::new(None),
        last_error: Mutex::new(String::new()),
    });

    tauri::Builder::default()
        .manage(state.clone())
        .invoke_handler(tauri::generate_handler![
            read_log,
            get_backend_status,
            restart_backend,
        ])
        .setup(move |app| {
            append_log("=== Biblical Study AI Launcher ===");

            kill_process_on_port(8000);
            thread::sleep(Duration::from_secs(1));

            let workdir = resolve_python_app(app.path_resolver())?;
            append_log(&format!("Workdir resolved: {:?}", workdir));

            start_backend(&workdir, &state)?;

            let backend_ok = wait_for_backend(20);
            if !backend_ok {
                let msg = "WARNING: Backend health check failed after 20s timeout";
                eprintln!("{}", msg);
                append_log(msg);
            } else {
                append_log("Backend health check passed.");
            }
            state.running.store(backend_ok, Ordering::SeqCst);

            // Launch background monitor
            let mon_state = state.clone();
            let mon_workdir = workdir.clone();
            start_monitor(mon_workdir, mon_state);

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
