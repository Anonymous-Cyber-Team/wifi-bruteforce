package com.hayyaalassalah.faizanahmad.wifihacker;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.widget.TextView;

import uk.co.chrisjenx.calligraphy.CalligraphyConfig;
import uk.co.chrisjenx.calligraphy.CalligraphyContextWrapper;

/**
 * Devil-X WiFi Bruteforce 2.0
 * Developer: MD Shamim | Devil-X Studios
 */
public class InstructionsClass extends Activity {

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        CalligraphyConfig.initDefault(new CalligraphyConfig.Builder()
                        .setDefaultFontPath("fonts/Lato-Light.ttf")
                        .setFontAttrId(R.attr.fontPath)
                        .build()
        );
        setContentView(R.layout.instruction_layout);
        TextView instruction = (TextView) findViewById(R.id.textView4);
        instruction.setText("🔥 Devil-X WiFi Bruteforce 2.0\nLead Developer: MD Shamim\nStudio: Devil-X Studios\n\n" +
                "নির্দেশিকা ও ব্যবহারের নিয়মাবলী:\n\n" +
                "১. আক্রমণ শুরুর আগে ফোনের ওয়াইফাই চালু করে নিন।\n" +
                "২. টার্গেট ওয়াইফাই রাউটারের সিগন্যাল যথেষ্ট শক্তিশালী হওয়া প্রয়োজন।\n" +
                "৩. WPA / WPA2 / WEP এনক্রিপশনের নেটওয়ার্কে পরীক্ষা করা যাবে।\n" +
                "৪. বেসিক প্ল্যানে অ্যাপের বিল্ট-ইন ১০,০০০ শীর্ষ পাসওয়ার্ড স্বয়ংক্রিয়ভাবে পরীক্ষা করা হয়।\n" +
                "৫. স্ট্যান্ডার্ড ও প্রো প্ল্যানে নিজস্ব পাসওয়ার্ড লিস্ট ও স্মার্ট প্রেডিকশন সক্রিয় থাকে।\n\n" +
                "যোগাযোগ ও সহায়তা:\n" +
                "Telegram: @shamim_vaiya\n" +
                "WhatsApp: +8801540580575\n" +
                "Email: shamimvaiyaofficial@gmail.com");
    }

    @Override
    protected void attachBaseContext(Context newBase) {
        super.attachBaseContext(CalligraphyContextWrapper.wrap(newBase));
    }
}
