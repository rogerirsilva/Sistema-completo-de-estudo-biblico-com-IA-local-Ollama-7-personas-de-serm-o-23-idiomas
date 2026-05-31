#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::fs;
use std::io;
use std::net::TcpStream;
use std::path::{Path, PathBuf};
use std::process::Command;

fn copy_dir_all(src: impl AsRef<Path>, dst: impl AsRef<Path>) -> io::Result<()> {
    fs::create_dir_all(dst.as_ref())?;
    for entry in fs::read_dir(src)? {
        let entry = entry?;
        let file_type = entry.file_type()?;
        let src_path = entry.path();
        let dst_path = dst.as_ref().join(entry.file_name());

        if file_type.is_dir() {
            copy_dir_all(src_path, dst_path)?;
        } else {
            fs::copy(src_path, dst_path)?;
        }
    }
    Ok(())
}

fn is_backend_running() -> bool {
    TcpStream::connect("127.0.0.1:8000").is_ok()
}

fn bootstrap_python_app(app: &tauri::App) -> io::Result<PathBuf> {
    let app_data = app
        .path_resolver()
        .app_data_dir()
        .ok_or_else(|| io::Error::new(io::ErrorKind::NotFound, "Could not resolve app data dir"))?;

    let target_dir = app_data.join("python_app");

    fs::create_dir_all(&target_dir)?;

    let resource_dir = app
        .path_resolver()
        .resource_dir()
        .ok_or_else(|| io::Error::new(io::ErrorKind::NotFound, "Could not resolve resource dir"))?;

    let mut source_dir = resource_dir.join("python_app");
    if !source_dir.exists() {
        let dev_fallback = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("..")
            .join("python_app");
        if dev_fallback.exists() {
            source_dir = dev_fallback;
        } else {
            return Err(io::Error::new(
                io::ErrorKind::NotFound,
                format!("Embedded python_app resources not found at {}", source_dir.display()),
            ));
        }
    }

    // Always sync bundled resources so fixes in start scripts are applied on next launch.
    copy_dir_all(&source_dir, &target_dir)?;

    Ok(target_dir)
}

#[cfg(target_os = "windows")]
fn start_backend(workdir: &Path) -> io::Result<()> {
    Command::new("cmd")
        .args(["/C", "call", "start_api.bat"])
        .current_dir(workdir)
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

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            if !is_backend_running() {
                let workdir = bootstrap_python_app(app)?;
                start_backend(&workdir)?;
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
