import os
import comtypes.client
import ctypes
from ctypes import wintypes

# Generate the SHDocVw type library
comtypes.client.GetModule("shdocvw.dll")

# Import the generated SHDocVw module
import comtypes.gen.SHDocVw as SHDocVw

# Define the GUID for IActiveDesktop
CLSID_ActiveDesktop = comtypes.GUID("{75048700-EF1F-11D0-9888-006097DEACF9}")
IID_IActiveDesktop = comtypes.GUID("{F490EB00-1240-11D1-9888-006097DEACF9}")


# Define the IActiveDesktop interface
class IActiveDesktop(comtypes.IUnknown):
    _iid_ = IID_IActiveDesktop
    _methods_ = [
        comtypes.STDMETHOD(ctypes.HRESULT, "ApplyChanges", [ctypes.c_ulong]),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "GetWallpaper",
            [wintypes.LPWSTR, ctypes.c_uint, ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT, "SetWallpaper", [wintypes.LPCWSTR, ctypes.c_ulong]
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "GetWallpaperOptions",
            [ctypes.POINTER(wintypes.LPVOID), ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "SetWallpaperOptions",
            [ctypes.POINTER(wintypes.LPVOID), ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "GetPattern",
            [wintypes.LPWSTR, ctypes.c_uint, ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT, "SetPattern", [wintypes.LPCWSTR, ctypes.c_ulong]
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "GetDesktopItemOptions",
            [ctypes.POINTER(wintypes.LPVOID), ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "SetDesktopItemOptions",
            [ctypes.POINTER(wintypes.LPVOID), ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "AddDesktopItem",
            [ctypes.POINTER(wintypes.LPVOID), ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "AddDesktopItemWithUI",
            [wintypes.HWND, ctypes.POINTER(wintypes.LPVOID), ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "ModifyDesktopItem",
            [ctypes.POINTER(wintypes.LPVOID), ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "RemoveDesktopItem",
            [ctypes.POINTER(wintypes.LPVOID), ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "GetDesktopItemByID",
            [ctypes.c_ulong, ctypes.POINTER(wintypes.LPVOID), ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "GetDesktopItemWithIDList",
            [
                ctypes.POINTER(wintypes.LPVOID),
                ctypes.c_ulong,
                ctypes.POINTER(wintypes.LPVOID),
                ctypes.c_ulong,
            ],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "GetDesktopItem",
            [ctypes.c_ulong, ctypes.POINTER(wintypes.LPVOID), ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "GetDesktopItemList",
            [ctypes.POINTER(wintypes.LPVOID), ctypes.c_ulong],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "GetDesktopItemState",
            [ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)],
        ),
        comtypes.STDMETHOD(
            ctypes.HRESULT,
            "SetDesktopItemState",
            [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong],
        ),
    ]


def get_active_desktop():
    # Initialize COM
    comtypes.CoInitialize()

    # Get the IShellDispatch2 interface from Shell.Application
    # shell = comtypes.client.CreateObject("Shell.Application")
    # shell_dispatch = shell.QueryInterface(SHDocVw.IShellDispatch)

    # Get the IActiveDesktop interface
    iad = comtypes.client.CreateObject(CLSID_ActiveDesktop, interface=IActiveDesktop)

    return iad


def set_wallpaper_per_monitor(wallpaper_paths):
    print("Avant get desktop")
    iad = get_active_desktop()
    print("Avant boucle pour bg")
    for i, wallpaper_path in enumerate(wallpaper_paths):
        print(wallpaper_path)
        iad.SetWallpaper(wallpaper_path, i)
        iad.ApplyChanges(0x0002)  # AD_APPLY_FORCE
    print("après boucle")
    # Uninitialize COM
    comtypes.CoUninitialize()
    print("fin")


if __name__ == "__main__":
    wallpaper_paths = [
        # Replace with your actual image paths
        r"C:\Users\Alexis\Documents\GitHub\WallpaperSwitch\Images\Aoi Ogata.png"
    ]
    set_wallpaper_per_monitor(wallpaper_paths)

    print(os.getlogin())
