# FAQ (Continuously Updated, Contributions Welcome)

## Usage Issues

### ❓ Unable to Configure vLLM on Windows

​	vLLM currently does not support running on Windows. You can deploy it using WSL or Docker. For more details, refer to the README in the docker directory.

​	Detailed deployment documentation will be updated later.

### ❓ How to Resolve Font Rendering Issues in Generated Charts?

​	The default chart styling uses standard sans-serif fonts (`DejaVu Sans`, `Arial`, `Helvetica`). If your environment lacks standard fonts or displays missing glyph boxes, ensure `fonts-dejavu` or TrueType fonts are installed and clear the matplotlib cache:

```bash
# Ubuntu / Debian
sudo apt-get install -y fonts-dejavu-core
rm -rf ~/.cache/matplotlib
```

