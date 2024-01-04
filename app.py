import time
import pygetwindow as gw
import subprocess
log_file_path = "activity_log.txt"

def get_active_window_info():
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            window_title = active_window.title
            if callable(window_title):
                window_title = window_title()
            if "Google Chrome" in window_title:
                url = get_chrome_url()
                return f"{time.strftime('%Y-%m-%d %H:%M:%S')} - In Chrome: {url}" if url else f"{time.strftime('%Y-%m-%d %H:%M:%S')} - In Chrome"
            elif "Safari" in window_title:
                url = get_safari_url()
                return f"{time.strftime('%Y-%m-%d %H:%M:%S')} - In Safari: {url}" if url else f"{time.strftime('%Y-%m-%d %H:%M:%S')} - In Safari"
            elif "Mozilla Firefox" in window_title:
                url = get_firefox_url()
                return f"{time.strftime('%Y-%m-%d %H:%M:%S')} - In Firefox: {url}" if url else f"{time.strftime('%Y-%m-%d %H:%M:%S')} - In Firefox"
            elif "Microsoft Edge" in window_title:
                url = get_edge_url()
                return f"{time.strftime('%Y-%m-%d %H:%M:%S')} - In Edge: {url}" if url else f"{time.strftime('%Y-%m-%d %H:%M:%S')} - In Edge"
            else:
                return f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Active Window: {window_title}"
            
        return f"{time.strftime('%Y-%m-%d %H:%M:%S')} - No active window"
    except Exception as e:
        log_error(f"Desktop: {e}")
        return None

def get_chrome_url():
    try:
        # Execute AppleScript to get the URL from the active Chrome tab
        script = 'tell application "Google Chrome" to get the URL of active tab of front window'
        url = subprocess.check_output(["osascript", "-e", script], universal_newlines=True).strip()
        return url
    except Exception as e:
        log_error(f"Error getting Chrome URL: {e}")
        return None

def get_safari_url():
    try:
        # Execute AppleScript to get the URL from the active Safari tab
        script = 'tell application "Safari" to get the URL of front document'
        url = subprocess.check_output(["osascript", "-e", script], universal_newlines=True).strip()
        return url
    except Exception as e:
        log_error(f"Error getting Safari URL: {e}")
        return None

def get_firefox_url():
    try:
        # Execute AppleScript to get the URL from the active Firefox tab
        script = 'tell application "Firefox" to get the URL of active tab of front window'
        url = subprocess.check_output(["osascript", "-e", script], universal_newlines=True).strip()
        return url
    except Exception as e:
        log_error(f"Error getting Firefox URL: {e}")
        return None

def get_edge_url():
    try:
        # Use pygetwindow to get the Edge window and its title
        edge_window = gw.getWindowsWithTitle("Microsoft Edge")[0]
        edge_title = edge_window.title
        return edge_title
    except Exception as e:
        log_error(f"Error getting Edge URL: {e}")
        return None
     
def log_activity_info(info):
    try:
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"{info}\n")
        print(info)
    except Exception as e:
        log_error(f"Error logging activity info: {e}")

def log_error(error):
    try:
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} [ERROR] - {error}\n")
        print(f"[ERROR] {error}")
    except Exception as e:
        print(f"Error logging error info: {e}")

def main():
    while True:
        try:
            active_window_info = get_active_window_info()
            log_activity_info(active_window_info)
            time.sleep(5)
        except KeyboardInterrupt:
            break
        except Exception as e:
            log_error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()