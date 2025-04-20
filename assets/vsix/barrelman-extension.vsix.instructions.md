# Build Instructions for VSIX

1. Make sure you have [vsce](https://code.visualstudio.com/api/working-with-extensions/publishing-extension) installed:

```bash
npm install -g vsce
```

2. Place the following in the extension directory:

   - package.json
   - barrelman.tmLanguage.json
   - barrelman-theme-dark.json
   - barrelman-theme-light.json

3. From within that directory:

```bash
vsce package
```

4. Distribute the .vsix or install with:

```bash
code --install-extension barrelman-syntax-1.0.0.vsix
```
