import { loader } from '@monaco-editor/react';

// Configure Monaco editor to use local resources
export function configureMonaco() {
    if (typeof window !== 'undefined') {
        // Use monaco-editor from local node_modules
        loader.config({
            paths: {
                vs: '/monaco-editor/min/vs'
            }
        });
    }
}
