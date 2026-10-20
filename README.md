<p align="center">
  <img src="safaa_logo.svg" width="96" alt="Safaa Browser Logo" />
</p>

# Safaa Browser

**Website:** [safaabrowser.com](https://safaabrowser.com)

**Safaa** (`com.safaa.browser`) is a privacy-focused, Muslim Android web browser built on Chromium and Brave Core, featuring built-in real-time background music removal ([**NoMusic**](https://github.com/mohamedsadiqaguenaou/NoMusic)), full built-in ad & tracker blocking (**Shields**), and always-on pornography & adult content blocking.

---

## Key Features

- **Built-in [NoMusic](https://github.com/mohamedsadiqaguenaou/NoMusic):** Removes background music from web videos in real time while keeping voices clear, with a one-tap toggle in the toolbar.
- **Built-in Shields Ad & Tracker Blocking:** Blocks ads, popups, and trackers out of the box.
- **Always-On Pornography & Adult Content Blocker:** Built-in DNS filtering and SafeSearch enabled by default to block pornography and adult websites.

---

## System Requirements (Building for Android `arm64`)

Building Chromium + Safaa for Android requires a Linux environment (Ubuntu 22.04 / 24.04 LTS, or **WSL2** on Windows):

- **OS:** Ubuntu 22.04+ (x86_64) or Windows 11 with WSL2 (Ubuntu)
- **RAM:** 16 GB+ recommended (12 GB minimum with 16 GB swap and `JOBS=6`)
- **Disk Space:** ~120 GB free ext4 disk space
- **Tools:**
  - Node.js 20+ / 24+ and `pnpm`
  - Python 3, Git, Curl, Zstandard (`zstd`), Ninja, and standard Chromium Linux/Android build dependencies

---

## 1. Initial Checkout & Setup

In your Linux / WSL2 terminal, create the workspace directory and clone this repository into `src/brave` (Chromium's build files reference `//brave/...` paths relative to `src/`):

```bash
mkdir -p ~/Safaa/src
cd ~/Safaa/src
git clone https://github.com/mohamedsadiqaguenaou/Safaa.git brave
cd ~/Safaa/src/brave
```

### Environment Setup (`~/Safaa/env.sh`)

If building inside WSL2, ensure Windows `PATH` entries (`/mnt/...`) are excluded so Windows `node.exe` or `python.exe` do not interfere with the Linux build:

```bash
cat << 'EOF' > ~/Safaa/env.sh
# Keep Windows programs out of the Linux build in WSL2
PATH="$(printf '%s' "$PATH" | tr ':' '\n' | grep -v '^/mnt/' | paste -sd: -)"
PATH="$HOME/.local/node/bin:$PATH"
export PATH
EOF
source ~/Safaa/env.sh
```

### Fetch Chromium & Android Dependencies

Install Node dependencies and run `init` to fetch the matching Chromium tree, Android SDK/NDK, and apply all patches in `patches/`:

```bash
source ~/Safaa/env.sh
cd ~/Safaa/src/brave
pnpm install
pnpm run init --target_os=android --target_arch=arm64 --no-history
```

> **Note:** `pnpm run init` is safe to re-run if interrupted; `gclient` will resume downloading where it left off. After pulling new changes to `patches/`, re-apply them with:
> ```bash
> pnpm run apply_patches
> ```

---

## 2. Building the Android APK (`Safaa-arm64.apk`)

### Option A: Optimized Official Release Build (32 GB+ RAM)

Builds the full official `Release` configuration (`is_official_build = true`, ThinLTO, R8/ProGuard optimization, `release` channel):

```bash
source ~/Safaa/env.sh
cd ~/Safaa/src/brave

JOBS="$(nproc)"
export SISO_LIMITS="local=$JOBS"
export JAVA_OPTS="-Xmx16G -Xms4G"
export NODE_OPTIONS="--max-old-space-size=16384"

pnpm run build Release \
  --channel=release \
  --target_os=android \
  --target_arch=arm64 \
  --target_android_output_format=apk \
  --gn=symbol_level:0 \
  --ninja=j:"$JOBS"
```

Output APK:
```text
~/Safaa/src/out/android_Release_arm64/apks/Safaa-arm64.apk
```

### Option B: Low-Memory `Static` Build (12–16 GB RAM)

Builds an optimized APK without ThinLTO so linking fits comfortably in 12–16 GB RAM:

```bash
source ~/Safaa/env.sh
cd ~/Safaa/src/brave

JOBS="${JOBS:-6}"
export SISO_LIMITS="local=$JOBS"
export JAVA_OPTS="-Xmx4G -Xms1G"
export NODE_OPTIONS="--max-old-space-size=8192"

pnpm run build Static \
  --target_os=android \
  --target_arch=arm64 \
  --target_android_output_format=apk \
  --gn=symbol_level:0 \
  --gn=dcheck_always_on:false \
  --ninja=j:"$JOBS"
```

Output APK:
```text
~/Safaa/src/out/android_Static_arm64/apks/Safaa-arm64.apk
```

---

## 3. Useful Development Commands

- **Regenerate & verify GN build files without a full build:**
  ```bash
  source ~/Safaa/env.sh
  cd ~/Safaa/src/brave
  pnpm run gn gen -C gncheck --target_os=android --target_arch=arm64
  pnpm run gn check -C gncheck '//brave/*'
  ```
- **Regenerate Chromium rewrite patches (`rewrite/**/*.yaml`):**
  ```bash
  PATH=~/Safaa/src/brave/vendor/depot_tools:$PATH vpython3 tools/cr/plaster.py apply <path-to-yaml>
  ```

---

## License

This project is licensed under the [Mozilla Public License 2.0](LICENSE).
