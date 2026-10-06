package com.hayyaalassalah.faizanahmad.wifihacker;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.security.MessageDigest;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class SplashActivity extends Activity {

    public static final String SALT_KEY = "DevilX@Shamim#Studio2026";
    public static final String LICENSE_URL = "https://raw.githubusercontent.com/Anonymous-Cyber-Team/wifi-bruteforce/main/secret_vault/license.json";
    private static final String PREFS_NAME = "devil_x_security";
    public static final String KEY_IS_UNLOCKED = "is_unlocked";
    public static final String KEY_EXPIRE_AT = "expire_at_timestamp";
    public static final String KEY_EXPIRE_STR = "expire_at_str";
    public static final String KEY_USERNAME = "licensed_username";
    public static final String KEY_PLAN = "licensed_plan";

    private SharedPreferences prefs;
    private EditText etUsername;
    private EditText etPassword;
    private TextView tvDeviceId;
    private String currentDeviceId = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        Toast.makeText(getApplicationContext(), "⚡ Devil-X Studios | MD Shamim ⚡", Toast.LENGTH_SHORT).show();

        // Fetch real, dynamic Android Device Hardware ID
        try {
            currentDeviceId = Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);
        } catch (Exception e) {
            currentDeviceId = "UNKNOWN_DEVICE";
        }

        prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        boolean isUnlocked = prefs.getBoolean(KEY_IS_UNLOCKED, false);
        long expireTimestamp = prefs.getLong(KEY_EXPIRE_AT, 0);

        long now = System.currentTimeMillis();
        if (isUnlocked && now < expireTimestamp) {
            String savedUser = prefs.getString(KEY_USERNAME, "User");
            Toast.makeText(this, "স্বাগতম, " + savedUser + "!", Toast.LENGTH_SHORT).show();
            goToMainActivity();
            return;
        }

        if (isUnlocked && now >= expireTimestamp) {
            Toast.makeText(this, "❌ আপনার লাইসেন্সের মেয়াদ শেষ হয়ে গেছে! অনুগ্রহ করে রিনিউ করুন।", Toast.LENGTH_LONG).show();
            prefs.edit().putBoolean(KEY_IS_UNLOCKED, false).apply();
        }

        final LinearLayout lockContainer = (LinearLayout) findViewById(R.id.lock_container);
        if (lockContainer != null) {
            lockContainer.setVisibility(View.VISIBLE);
        }

        etUsername = (EditText) findViewById(R.id.et_username);
        etPassword = (EditText) findViewById(R.id.et_password);
        tvDeviceId = (TextView) findViewById(R.id.tv_device_id);
        Button btnCopyId = (Button) findViewById(R.id.btn_copy_device_id);
        Button btnVerify = (Button) findViewById(R.id.btn_verify);

        if (tvDeviceId != null) {
            tvDeviceId.setText("Device ID: " + currentDeviceId);
        }

        if (btnCopyId != null) {
            btnCopyId.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                    ClipData clip = ClipData.newPlainText("Device ID", currentDeviceId);
                    if (clipboard != null) {
                        clipboard.setPrimaryClip(clip);
                        Toast.makeText(SplashActivity.this, "✅ ডিভাইস আইডি কপি হয়েছে!", Toast.LENGTH_SHORT).show();
                    }
                }
            });
        }

        if (btnVerify != null) {
            btnVerify.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    String username = etUsername.getText().toString().trim();
                    String password = etPassword.getText().toString().trim();

                    if (username.isEmpty()) {
                        Toast.makeText(SplashActivity.this, "ইউজারনেম লিখুন!", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    if (password.isEmpty()) {
                        Toast.makeText(SplashActivity.this, "পাসওয়ার্ড লিখুন!", Toast.LENGTH_SHORT).show();
                        return;
                    }

                    new LicenseCheckTask(username, password).execute(LICENSE_URL);
                }
            });
        }
    }

    private class LicenseCheckTask extends AsyncTask<String, Void, String> {
        private String username;
        private String password;
        private ProgressDialog dialog;
        private boolean success = false;
        private String message = "";
        private String verifiedPlan = "Basic";

        public LicenseCheckTask(String username, String password) {
            this.username = username;
            this.password = password;
        }

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            dialog = new ProgressDialog(SplashActivity.this);
            dialog.setMessage("Devil-X লাইসেন্স ভেরিফাই করা হচ্ছে...");
            dialog.setCancelable(false);
            dialog.show();
        }

        @Override
        protected String doInBackground(String... params) {
            HttpURLConnection conn = null;
            BufferedReader reader = null;
            try {
                URL url = new URL(params[0]);
                conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(8000);
                conn.setReadTimeout(8000);

                if (conn.getResponseCode() != 200) {
                    message = "সার্ভারের সাথে সংযোগ ব্যর্থ হয়েছে (Code: " + conn.getResponseCode() + ")!";
                    return null;
                }

                reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    sb.append(line);
                }

                JSONObject root = new JSONObject(sb.toString());
                if (!root.has("users")) {
                    message = "লাইসেন্স ডাটাবেজ ফরম্যাট সঠিক নয়!";
                    return null;
                }

                JSONObject users = root.getJSONObject("users");
                if (!users.has(username)) {
                    message = "❌ ইউজারনেম পাওয়া যায়নি!";
                    return null;
                }

                JSONObject userObj = users.getJSONObject(username);
                String expectedHash = userObj.optString("password_hash", "");
                String status = userObj.optString("status", "active");
                String expireAtStr = userObj.optString("expire_date", userObj.optString("expire_at", ""));
                String lockedDeviceId = userObj.optString("device_id", "").trim();
                verifiedPlan = userObj.optString("plan", "Basic");

                if (!status.equalsIgnoreCase("active")) {
                    message = "❌ এই ইউজারের এক্সেস স্থগিত (Blocked) করা আছে!";
                    return null;
                }

                // Device locking validation
                if (!lockedDeviceId.isEmpty() && !lockedDeviceId.equalsIgnoreCase(currentDeviceId)) {
                    message = "❌ এই লাইসেন্সটি অন্য একটি ডিভাইসে সক্রিয় আছে!";
                    return null;
                }

                // Verify password + salt hash
                String inputHash = sha256(password + SALT_KEY);
                if (!expectedHash.equalsIgnoreCase(inputHash)) {
                    message = "❌ ভুল পাসওয়ার্ড! সঠিক পাসওয়ার্ড দিন।";
                    return null;
                }

                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.US);
                Date expireDate = sdf.parse(expireAtStr);
                long expireTimestamp = expireDate.getTime();
                long now = System.currentTimeMillis();

                if (now > expireTimestamp) {
                    message = "❌ এই লাইসেন্সের মেয়াদ " + expireAtStr + " তারিখে শেষ হয়ে গেছে!";
                    return null;
                }

                // Valid license!
                prefs.edit()
                    .putBoolean(KEY_IS_UNLOCKED, true)
                    .putLong(KEY_EXPIRE_AT, expireTimestamp)
                    .putString(KEY_EXPIRE_STR, expireAtStr)
                    .putString(KEY_USERNAME, username)
                    .putString(KEY_PLAN, verifiedPlan)
                    .apply();

                success = true;
                message = "✅ সফলভাবে আনলক হয়েছে!\nস্বাগতম: " + username + " (" + verifiedPlan + " Plan)";
                return "OK";

            } catch (Exception e) {
                message = "যাচাইকরণে ত্রুটি: " + e.getMessage();
                return null;
            } finally {
                if (reader != null) {
                    try { reader.close(); } catch (Exception ignored) {}
                }
                if (conn != null) {
                    conn.disconnect();
                }
            }
        }

        @Override
        protected void onPostExecute(String result) {
            if (dialog != null && dialog.isShowing()) {
                dialog.dismiss();
            }

            Toast.makeText(SplashActivity.this, message, Toast.LENGTH_LONG).show();

            if (success) {
                goToMainActivity();
            }
        }
    }

    private void goToMainActivity() {
        Intent i = new Intent(SplashActivity.this, MainActivity.class);
        startActivity(i);
        finish();
    }

    private static String sha256(String base) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(base.getBytes("UTF-8"));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (Exception ex) {
            return "";
        }
    }
}
