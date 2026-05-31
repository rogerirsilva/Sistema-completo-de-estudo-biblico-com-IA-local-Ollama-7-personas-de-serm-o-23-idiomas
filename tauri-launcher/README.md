# Tauri Desktop Launcher

This folder packages the Python FastAPI backend with a native Tauri desktop frontend.

## What it does

- On startup, the Tauri app copies `python_app` resources to user app-data.
- It starts the Python backend (`start_api.bat` on Windows, `start_api.sh` on Linux/macOS).
- The Tauri UI calls FastAPI endpoints directly at `http://localhost:8000`.

## Scripts (from project root)

- Test without installer (dev mode): `tauri_test_no_install.bat`
- Build installer for current OS: `tauri_build_installers.bat`

## Important

- Tauri cannot produce Windows, Linux and macOS binaries from one machine by default.
- Run build on each target OS:
  - Windows: run `tauri_build_installers.bat`
  - Linux: run `npm run tauri:build` in `tauri-launcher`
  - macOS: run `npm run tauri:build` in `tauri-launcher`

## Toolchain prerequisites

- Node.js LTS
- Rust (cargo/rustup)
- Tauri OS dependencies:
  - Windows: WebView2 (usually preinstalled in Win11)
  - Linux: GTK/WebKit2GTK libs
  - macOS: Xcode Command Line Tools
