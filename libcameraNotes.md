# `libcamera` and `Picamera2` notes

## Arducam / pivariety cameras

* We're using the no-ir version of the imx519 sensor
* <https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/16MP-IMX519/>
* <https://www.raspberrypi.com/documentation/accessories/camera.html#getting-started>

## `libcamera`

> At Arducam, we added more RPI camera support and improved the existing libcamera with extensive features like auto-focus, external trigger, strobe functions, auto-load camera calibration parameters with our Pivariety solution and modified version of libcamera.

<https://libcamera.org>


<https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Libcamera-User-Guide/>

## `Picamera2`

<https://github.com/raspberrypi/picamera2>

<https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf>

<https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/PiCamera2-User-Guide/>

<https://github.com/ArduCAM/picamera2_examples>

### `libcamera-hello`

```
flip@pie:~/FIP-2023 $ libcamera-hello --list-cameras
Available cameras
-----------------
0 : imx519 [4656x3496] (/base/soc/i2c0mux/i2c@1/imx519@1a)
    Modes: 'SRGGB10_CSI2P' : 1280x720 [80.01 fps - (1048, 1042)/2560x1440 crop]
                             1920x1080 [60.05 fps - (408, 674)/3840x2160 crop]
                             2328x1748 [30.00 fps - (0, 0)/4656x3496 crop]
                             3840x2160 [18.00 fps - (408, 672)/3840x2160 crop]
                             4656x3496 [9.00 fps - (0, 0)/4656x3496 crop]
```

### LEDs and Filters

* Edmund IR-pass filters at about 720nm
* Random LEDs from fp's drawers that are around 800nm (measured @ bob's lab)
