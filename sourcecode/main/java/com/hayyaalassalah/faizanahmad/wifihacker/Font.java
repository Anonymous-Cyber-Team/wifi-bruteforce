package com.hayyaalassalah.faizanahmad.wifihacker;

import android.app.Application;

import uk.co.chrisjenx.calligraphy.CalligraphyConfig;

/**
 * Devil-X WiFi Bruteforce 2.0
 * Developer: MD Shamim | Devil-X Studios
 */
public class Font extends Application {
    @Override
    public void onCreate() {
        super.onCreate();

        CalligraphyConfig.initDefault(new CalligraphyConfig.Builder()
                        .setDefaultFontPath("Lato-Light.ttf")
                        .setFontAttrId(R.attr.fontPath)
                        .build()
        );
    }
}