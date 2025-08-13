"""
Configuration Manager for Ragnarok X Auto Fishing Bot
Handles saving/loading settings, profiles, and user preferences
"""

import configparser
import json
import os
from datetime import datetime
import shutil

class ConfigManager:
    def __init__(self, config_dir="config"):
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "fishing_config.ini")
        self.profiles_dir = os.path.join(config_dir, "profiles")
        self.current_profile = "default"
        
        self.ensure_directories()
        self.config = configparser.ConfigParser()
        self.load_default_config()
        
    def ensure_directories(self):
        """Create necessary directories"""
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.profiles_dir, exist_ok=True)
        
    def load_default_config(self):
        """Load default configuration"""
        self.config.clear()
        
        # Default coordinates
        self.config['Coordinates'] = {
            'cast_button_x': '400',
            'cast_button_y': '500', 
            'fishing_area_x': '400',
            'fishing_area_y': '300',
            'fishing_region_width': '200',
            'fishing_region_height': '200'
        }
        
        # Default timing settings
        self.config['Timing'] = {
            'cast_delay_min': '2.0',
            'cast_delay_max': '4.0',
            'bite_timeout': '30',
            'reaction_time_min': '0.3',
            'reaction_time_max': '0.8',
            'hook_hold_duration': '1.0'
        }
        
        # Default detection settings
        self.config['Detection'] = {
            'hook_sensitivity': '0.8',
            'motion_sensitivity': '20',
            'color_change_threshold': '0.05',
            'template_confidence': '0.7',
            'use_motion_detection': 'True',
            'use_color_detection': 'True',
            'use_template_matching': 'True'
        }
        
        # Default safety settings
        self.config['Safety'] = {
            'randomize_timings': 'True',
            'anti_detection_enabled': 'True',
            'break_interval_minutes': '30',
            'break_duration_min': '30',
            'break_duration_max': '120',
            'max_session_hours': '4',
            'mouse_movement_variation': '20'
        }
        
        # Default interface settings
        self.config['Interface'] = {
            'window_width': '800',
            'window_height': '700',
            'log_max_lines': '1000',
            'auto_save_config': 'True',
            'show_debug_info': 'False',
            'enable_sound_alerts': 'True'
        }
        
        # Default hotkeys
        self.config['Hotkeys'] = {
            'start_stop': 'F1',
            'pause_resume': 'F2', 
            'emergency_stop': 'F4',
            'save_screenshot': 'F5'
        }
        
        # Statistics tracking
        self.config['Statistics'] = {
            'total_fish_caught': '0',
            'total_casts_made': '0',
            'total_runtime_hours': '0.0',
            'best_session_fish': '0',
            'sessions_completed': '0'
        }
        
    def save_config(self, filename=None):
        """Save current configuration to file"""
        try:
            if filename is None:
                filename = self.config_file
                
            with open(filename, 'w') as f:
                self.config.write(f)
                
            return True
            
        except Exception as e:
            print(f"Error saving config: {str(e)}")
            return False
            
    def load_config(self, filename=None):
        """Load configuration from file"""
        try:
            if filename is None:
                filename = self.config_file
                
            if os.path.exists(filename):
                self.config.read(filename)
                return True
            else:
                print(f"Config file not found: {filename}")
                return False
                
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            return False
            
    def get(self, section, option, fallback=None):
        """Get configuration value with fallback"""
        try:
            return self.config.get(section, option, fallback=fallback)
        except:
            return fallback
            
    def getint(self, section, option, fallback=0):
        """Get integer configuration value with fallback"""
        try:
            return self.config.getint(section, option, fallback=fallback)
        except:
            return fallback
            
    def getfloat(self, section, option, fallback=0.0):
        """Get float configuration value with fallback"""
        try:
            return self.config.getfloat(section, option, fallback=fallback)
        except:
            return fallback
            
    def getboolean(self, section, option, fallback=False):
        """Get boolean configuration value with fallback"""
        try:
            return self.config.getboolean(section, option, fallback=fallback)
        except:
            return fallback
            
    def set(self, section, option, value):
        """Set configuration value"""
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, option, str(value))
            return True
        except Exception as e:
            print(f"Error setting config value: {str(e)}")
            return False
            
    def save_profile(self, profile_name, description=""):
        """Save current configuration as a named profile"""
        try:
            profile_file = os.path.join(self.profiles_dir, f"{profile_name}.ini")
            
            # Add profile metadata
            if not self.config.has_section('Profile'):
                self.config.add_section('Profile')
                
            self.config.set('Profile', 'name', profile_name)
            self.config.set('Profile', 'description', description)
            self.config.set('Profile', 'created_date', datetime.now().isoformat())
            
            # Save to profile file
            with open(profile_file, 'w') as f:
                self.config.write(f)
                
            return True
            
        except Exception as e:
            print(f"Error saving profile: {str(e)}")
            return False
            
    def load_profile(self, profile_name):
        """Load a named profile"""
        try:
            profile_file = os.path.join(self.profiles_dir, f"{profile_name}.ini")
            
            if os.path.exists(profile_file):
                self.config.read(profile_file)
                self.current_profile = profile_name
                return True
            else:
                print(f"Profile not found: {profile_name}")
                return False
                
        except Exception as e:
            print(f"Error loading profile: {str(e)}")
            return False
            
    def get_available_profiles(self):
        """Get list of available profiles"""
        try:
            profiles = []
            
            for filename in os.listdir(self.profiles_dir):
                if filename.endswith('.ini'):
                    profile_name = filename[:-4]  # Remove .ini extension
                    
                    # Try to get profile info
                    temp_config = configparser.ConfigParser()
                    profile_path = os.path.join(self.profiles_dir, filename)
                    temp_config.read(profile_path)
                    
                    profile_info = {
                        'name': profile_name,
                        'description': temp_config.get('Profile', 'description', fallback=''),
                        'created_date': temp_config.get('Profile', 'created_date', fallback='Unknown')
                    }
                    
                    profiles.append(profile_info)
                    
            return profiles
            
        except Exception as e:
            print(f"Error getting profiles: {str(e)}")
            return []
            
    def delete_profile(self, profile_name):
        """Delete a named profile"""
        try:
            if profile_name == 'default':
                print("Cannot delete default profile")
                return False
                
            profile_file = os.path.join(self.profiles_dir, f"{profile_name}.ini")
            
            if os.path.exists(profile_file):
                os.remove(profile_file)
                return True
            else:
                print(f"Profile not found: {profile_name}")
                return False
                
        except Exception as e:
            print(f"Error deleting profile: {str(e)}")
            return False
            
    def export_config(self, export_path):
        """Export current configuration to specified path"""
        try:
            shutil.copy2(self.config_file, export_path)
            return True
        except Exception as e:
            print(f"Error exporting config: {str(e)}")
            return False
            
    def import_config(self, import_path):
        """Import configuration from specified path"""
        try:
            if os.path.exists(import_path):
                shutil.copy2(import_path, self.config_file)
                self.load_config()
                return True
            else:
                print(f"Import file not found: {import_path}")
                return False
        except Exception as e:
            print(f"Error importing config: {str(e)}")
            return False
            
    def backup_config(self):
        """Create a backup of current configuration"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.config_dir, f"backup_{timestamp}.ini")
            shutil.copy2(self.config_file, backup_file)
            
            # Keep only last 10 backups
            self.cleanup_old_backups()
            
            return backup_file
            
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            return None
            
    def cleanup_old_backups(self, keep_count=10):
        """Remove old backup files, keeping only the most recent ones"""
        try:
            backups = []
            
            for filename in os.listdir(self.config_dir):
                if filename.startswith('backup_') and filename.endswith('.ini'):
                    filepath = os.path.join(self.config_dir, filename)
                    backups.append((os.path.getmtime(filepath), filepath))
                    
            # Sort by modification time (newest first)
            backups.sort(reverse=True)
            
            # Remove old backups
            for i, (mtime, filepath) in enumerate(backups):
                if i >= keep_count:
                    os.remove(filepath)
                    
        except Exception as e:
            print(f"Error cleaning up backups: {str(e)}")
            
    def update_statistics(self, fish_caught=0, casts_made=0, session_time=0):
        """Update fishing statistics"""
        try:
            # Get current values
            total_fish = self.getint('Statistics', 'total_fish_caught', 0)
            total_casts = self.getint('Statistics', 'total_casts_made', 0)
            total_hours = self.getfloat('Statistics', 'total_runtime_hours', 0.0)
            best_session = self.getint('Statistics', 'best_session_fish', 0)
            sessions = self.getint('Statistics', 'sessions_completed', 0)
            
            # Update values
            total_fish += fish_caught
            total_casts += casts_made
            total_hours += session_time / 3600.0  # Convert seconds to hours
            
            if fish_caught > best_session:
                best_session = fish_caught
                
            if session_time > 0:  # Only increment if it was a real session
                sessions += 1
                
            # Save updated values
            self.set('Statistics', 'total_fish_caught', total_fish)
            self.set('Statistics', 'total_casts_made', total_casts)
            self.set('Statistics', 'total_runtime_hours', f"{total_hours:.2f}")
            self.set('Statistics', 'best_session_fish', best_session)
            self.set('Statistics', 'sessions_completed', sessions)
            
            return True
            
        except Exception as e:
            print(f"Error updating statistics: {str(e)}")
            return False
            
    def get_statistics_summary(self):
        """Get formatted statistics summary"""
        try:
            total_fish = self.getint('Statistics', 'total_fish_caught', 0)
            total_casts = self.getint('Statistics', 'total_casts_made', 0)
            total_hours = self.getfloat('Statistics', 'total_runtime_hours', 0.0)
            best_session = self.getint('Statistics', 'best_session_fish', 0)
            sessions = self.getint('Statistics', 'sessions_completed', 0)
            
            # Calculate derived statistics
            success_rate = (total_fish / total_casts * 100) if total_casts > 0 else 0
            fish_per_hour = (total_fish / total_hours) if total_hours > 0 else 0
            avg_session_fish = (total_fish / sessions) if sessions > 0 else 0
            
            return {
                'total_fish_caught': total_fish,
                'total_casts_made': total_casts,
                'total_runtime_hours': total_hours,
                'best_session_fish': best_session,
                'sessions_completed': sessions,
                'overall_success_rate': success_rate,
                'fish_per_hour': fish_per_hour,
                'average_session_fish': avg_session_fish
            }
            
        except Exception as e:
            print(f"Error getting statistics: {str(e)}")
            return {}
            
    def reset_statistics(self):
        """Reset all statistics to zero"""
        try:
            self.set('Statistics', 'total_fish_caught', '0')
            self.set('Statistics', 'total_casts_made', '0') 
            self.set('Statistics', 'total_runtime_hours', '0.0')
            self.set('Statistics', 'best_session_fish', '0')
            self.set('Statistics', 'sessions_completed', '0')
            return True
        except Exception as e:
            print(f"Error resetting statistics: {str(e)}")
            return False
            
    def validate_config(self):
        """Validate current configuration for common issues"""
        issues = []
        
        try:
            # Check coordinates
            cast_x = self.getint('Coordinates', 'cast_button_x', 0)
            cast_y = self.getint('Coordinates', 'cast_button_y', 0)
            
            if cast_x <= 0 or cast_y <= 0:
                issues.append("Invalid cast button coordinates")
                
            # Check timing values
            cast_min = self.getfloat('Timing', 'cast_delay_min', 0)
            cast_max = self.getfloat('Timing', 'cast_delay_max', 0)
            
            if cast_min >= cast_max:
                issues.append("Cast delay minimum must be less than maximum")
                
            # Check sensitivity values
            sensitivity = self.getfloat('Detection', 'hook_sensitivity', 0)
            
            if sensitivity < 0.1 or sensitivity > 1.0:
                issues.append("Hook sensitivity must be between 0.1 and 1.0")
                
            return issues
            
        except Exception as e:
            issues.append(f"Config validation error: {str(e)}")
            return issues

# Example usage and testing
if __name__ == "__main__":
    config_mgr = ConfigManager()
    
    # Test basic functionality
    print("Testing ConfigManager...")
    
    # Save default config
    config_mgr.save_config()
    print("Default config saved")
    
    # Test profile management
    config_mgr.save_profile("test_profile", "Test profile for debugging")
    profiles = config_mgr.get_available_profiles()
    print(f"Available profiles: {[p['name'] for p in profiles]}")
    
    # Test statistics
    config_mgr.update_statistics(fish_caught=5, casts_made=10, session_time=3600)
    stats = config_mgr.get_statistics_summary()
    print(f"Statistics: {stats}")
    
    # Test validation
    issues = config_mgr.validate_config()
    if issues:
        print(f"Config issues found: {issues}")
    else:
        print("Configuration is valid")
        
    print("ConfigManager testing complete!")
