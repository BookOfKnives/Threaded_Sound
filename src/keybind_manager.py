import keyboard


class KeybindManager:
    """Manages global keyboard bindings for sound panels - supports multiple callbacks per keybind"""
    
    def __init__(self):
        self.registered_hotkeys = {}  # keybind -> list of callbacks mapping
        self.callback_to_keybind = {}  # callback -> keybind mapping for removal
    
    def register(self, keybind, callback):
        """Register a global hotkey with a callback - multiple callbacks can share the same keybind"""
        if not keybind:
            return
        
        # If this is a new keybind, register it with keyboard library
        if keybind not in self.registered_hotkeys:
            try:
                keyboard.add_hotkey(keybind, lambda k=keybind: self._trigger_callbacks(k), suppress=False)
                self.registered_hotkeys[keybind] = []
            except Exception as e:
                return
        
        # Add callback to the list for this keybind
        if callback not in self.registered_hotkeys[keybind]:
            self.registered_hotkeys[keybind].append(callback)
            self.callback_to_keybind[callback] = keybind
    
    def _trigger_callbacks(self, keybind):
        """Trigger all callbacks associated with a keybind"""
        if keybind in self.registered_hotkeys:
            for callback in self.registered_hotkeys[keybind]:
                try:
                    callback()
                except Exception as e:
                    pass
    
    def unregister(self, callback):
        """Unregister a specific callback"""
        if callback not in self.callback_to_keybind:
            return
        
        keybind = self.callback_to_keybind[callback]
        
        # Remove callback from the list
        if keybind in self.registered_hotkeys and callback in self.registered_hotkeys[keybind]:
            self.registered_hotkeys[keybind].remove(callback)
            del self.callback_to_keybind[callback]
            
            # If no more callbacks for this keybind, remove the hotkey
            if not self.registered_hotkeys[keybind]:
                try:
                    keyboard.remove_hotkey(keybind)
                    del self.registered_hotkeys[keybind]
                except Exception as e:
                    pass
    
    def update(self, callback, old_keybind, new_keybind):
        """Update a callback's keybind by removing from old and registering to new"""
        # Remove callback from old keybind
        if callback in self.callback_to_keybind:
            self.unregister(callback)
        
        # Register callback to new keybind
        if new_keybind:
            self.register(new_keybind, callback)
    
    def cleanup(self):
        """Remove all registered hotkeys"""
        keyboard.unhook_all()
        self.registered_hotkeys.clear()
