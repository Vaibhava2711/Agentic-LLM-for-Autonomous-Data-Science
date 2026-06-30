#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Source and destination paths
const sourceDir = path.join(__dirname, '..', 'node_modules', 'monaco-editor', 'min');
const targetDir = path.join(__dirname, '..', 'public', 'monaco-editor', 'min');

// Recursively copy directory
function copyDir(src, dest) {
    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
    }

    const entries = fs.readdirSync(src, { withFileTypes: true });

    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);

        if (entry.isDirectory()) {
            copyDir(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    }
}

console.log('Setting up Monaco Editor resources...');

try {
    if (!fs.existsSync(sourceDir)) {
        console.error('Error: Monaco Editor source directory not found.');
        console.error('Please ensure monaco-editor is installed: npm install monaco-editor');
        process.exit(1);
    }

    copyDir(sourceDir, targetDir);
    console.log('✓ Monaco Editor resources copied successfully to public/monaco-editor/min');
} catch (error) {
    console.error('Error setting up Monaco Editor:', error);
    process.exit(1);
}
