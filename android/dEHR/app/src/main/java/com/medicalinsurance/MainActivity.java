package com.medicalinsurance;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;

import com.medicalinsurance.protobuf.Payload;
import com.google.android.material.textfield.TextInputEditText;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.protobuf.InvalidProtocolBufferException;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
//import androidx.annotation.NonNull;
import androidx.multidex.MultiDex;

import android.text.method.ScrollingMovementMethod;
import android.util.Log;
//import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Random;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import sawtooth.sdk.signing.PrivateKey;
import sawtooth.sdk.signing.Secp256k1Context;
import sawtooth.sdk.signing.Secp256k1PrivateKey;
import android.util.Base64;

public class MainActivity extends AppCompatActivity {
//    private TextView mTextMessage;
    private TextView  mTextViewResult;
    private TextView mTextDoctorPKey;
    private TextInputEditText mEditTextURL;
    public static final String DEHR_PREFS_NAME = "dEHRPrefsFile";
    public static final String PARAM_NAME_URL = "RestApiURL";
    public static final String PARAM_NAME_PATIENT_PKEY = "PatientPKey";
    public static final String PARAM_NAME_DOCTOR_PKEY = "DoctorPKey";
//    public static final String PARAM_NAME_GRANT_ACCESS = "DoctorAccessGranted";
    public static final String DEHR_PRIVATE_KEY = "private_key";
    public static final String DEHR_PUBLIC_KEY = "public_key";
    public static final String DEHR_REST_API_DEFAULT = "http://localhost:8040";
    public static final int MY_CAMERA_REQUEST_CODE = 6515;
    public static final String QR_CODE_ENTERED_VALUE = "QR_CODE_ENTERED_VALUE";

//    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
//            = new BottomNavigationView.OnNavigationItemSelectedListener() {
//
//        @Override
//        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
//            switch (item.getItemId()) {
//                case R.id.navigation_home:
//                    mTextMessage.setText(R.string.title_home);
//                    return true;
//                case R.id.navigation_dashboard:
//                    mTextMessage.setText(R.string.title_dashboard);
//                    return true;
//                case R.id.navigation_notifications:
//                    mTextMessage.setText(R.string.title_notifications);
//                    return true;
//            }
//            return false;
//        }
//    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        init();
//        BottomNavigationView navView = findViewById(R.id.nav_view);
//        mTextMessage = findViewById(R.id.message);
        Button mButtonRevokeAccess = findViewById(R.id.btn_revoke_access);
        Button mButtonGrantAccess = findViewById(R.id.btn_grant_access);
        mTextViewResult = findViewById(R.id.text_view_result);
        mTextViewResult.setMovementMethod(new ScrollingMovementMethod());
        Button mButtonSetURL = findViewById(R.id.btn_set_rest_api);
        Button mButtonGetItems = findViewById(R.id.btn_get_items);
        Button mButtonAddPulse = findViewById(R.id.btn_add_pulse);
//        Button mButtonScanQRCode = findViewById(R.id.btn_scan_qr_code);
        mEditTextURL = findViewById(R.id.edit_rest_api_url);
        Button mButtonScanQRCode = findViewById(R.id.btn_scan_qr_code);
        Button mButtonRegisterPatient = findViewById(R.id.btn_register_patient);
        //Check button states
        SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
        String restoredText = prefs.getString(PARAM_NAME_URL, DEHR_REST_API_DEFAULT);
        mEditTextURL.setText(restoredText);
        mTextDoctorPKey = findViewById(R.id.text_doctor_pkey);
        initDoctorPKeyValue();
        //Save URL
        mButtonSetURL.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                SharedPreferences.Editor editor = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE).edit();
                String newURL = Objects.requireNonNull(mEditTextURL.getText()).toString();
                editor.putString(PARAM_NAME_URL, newURL);
                editor.apply();
                Log.d("SET_URL", newURL);
                Toast.makeText(MainActivity.this, newURL + " is set", Toast.LENGTH_SHORT).show();
            }
        });
        //Get items
        mButtonGetItems.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                OkHttpClient client = new OkHttpClient();
                String urlSuff = "/state?address=" + Addressing.makePulseListAddress();
                SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
                String url = prefs.getString(PARAM_NAME_URL, DEHR_REST_API_DEFAULT);

                Log.d("GET_ITEMS", url);
                Request request = new Request.Builder()
                        .url(url + urlSuff)
                        .get()
                        .build();

                client.newCall(request).enqueue(new Callback() {

                    @Override
                    public void onFailure(@Nullable Call call, @Nullable IOException e) {
                        if (e != null) {
                            e.printStackTrace();
                        }
                        final String myError = (e != null)?e.getMessage():"Null value";
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                mTextViewResult.setText(myError);
                                Toast.makeText(MainActivity.this, myError, Toast.LENGTH_SHORT).show();
                            }
                        });
                    }

                    @Override
                    public void onResponse(@Nullable Call call, @Nullable final Response response) throws IOException {
                        StringBuilder sb = new StringBuilder();
                        if(response != null && response.body() != null){
                            final String myResponse = response.body().string();
                            Map<String, Pulse> pulseList = new HashMap<>();
                            JsonObject jsonObject = new JsonParser().parse(myResponse).getAsJsonObject();
                            JsonArray jsonPulseList = jsonObject.getAsJsonArray("data");
                            for (JsonElement el : jsonPulseList) {
                                String address = el.getAsJsonObject().get("address").getAsString();
                                String data = el.getAsJsonObject().get("data").getAsString();
                                byte[] decodedBytes = Base64.decode(data, Base64.DEFAULT);
                                Payload.AddPulse cl;
                                try {
                                    cl = Payload.AddPulse.parseFrom(decodedBytes);
                                    pulseList.put(address, new Pulse(cl.getId(), cl.getClientPkey(), Integer.parseInt(cl.getPulse()), Long.parseLong(cl.getTimestamp())));
                                } catch (InvalidProtocolBufferException e) {
                                    pulseList.put(address, new Pulse("-1", "-1", -1, -1));
                                    e.printStackTrace();
                                }

                            }
                            for (Map.Entry<String, Pulse> entry : pulseList.entrySet()) {
                                sb.append("Address: ")
                                        .append(entry.getKey())
                                        .append("; Value: ")
                                        .append(entry.getValue().toString())
                                        .append(System.getProperty("line.separator"));
                            }
                        }
                        final String output = (response != null && response.body() != null)?sb.toString():"Null value";
                        MainActivity.this.runOnUiThread(new Runnable() {
                            @Override
                            public void run() {

                                mTextViewResult.setText(output);
                            }
                        });
//                        }
                    }
                });
            }
        });
        //Add Pulse
        mButtonAddPulse.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                OkHttpClient client = new OkHttpClient();

//                String url = "https://reqres.in/api/users?page=2";

                DEHRRequestHandler requestHandler = new DEHRRequestHandler(getPrivateKey());
                try {
//                    Date date= new Date();
//                    long time = date.getTime();
//                    final Timestamp ts = new Timestamp(time);
                    final long ts = Addressing.getCurrentTimestamp();
                    Random rand = new Random();
                    final int n = rand.nextInt(50);
                    byte[] pulseBody = requestHandler.addPulse(String.valueOf(ts), n, ts).toByteArray();
                    RequestBody body = RequestBody.create(MediaType.parse("application/octet-stream"), pulseBody);

                    SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
                    String url = prefs.getString(PARAM_NAME_URL, DEHR_REST_API_DEFAULT);
                    Log.d("ADD_PULSE", url);
                    String urlSuff = "/batches";
                    Request request = new Request.Builder()
                            .url(url + urlSuff)
                            .post(body)
                            .build();

                    client.newCall(request).enqueue(new Callback() {

                        @Override
                        public void onFailure(@Nullable Call call, @Nullable IOException e) {
                            if (e != null) {
                                e.printStackTrace();
                            }
                            final String myError = (e != null)?e.getMessage():"Null value";
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    mTextViewResult.setText(myError);
                                    Toast.makeText(MainActivity.this, myError, Toast.LENGTH_SHORT).show();
                                }
                            });
                        }

                        @Override
                        public void onResponse(@Nullable Call call, @Nullable Response response) throws IOException {
                            final String myResponse = (response != null && response.body() != null) ? response.body().string() : "Null value";
                            Log.d("ADD_PULSE", myResponse);
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    mTextViewResult.setText(myResponse);
                                    String msg = "Pulse: " + n + ", Timestamp: " + ts + " sent";
                                    Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                                }
                            });
                        }
                    });
                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
        });
        mButtonScanQRCode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, ScanQrCodeActivity.class);
                startActivityForResult(intent, MY_CAMERA_REQUEST_CODE);
            }
        });
        //Register patient
        mButtonRegisterPatient.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
//                SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
//                String pKey = prefs.getString(PARAM_NAME_PATIENT_PKEY, null);
//                if(pKey != null){
//                    Toast.makeText(MainActivity.this, "Patient already registered", Toast.LENGTH_SHORT).show();
//                    return;
//                }

                OkHttpClient client = new OkHttpClient();

                DEHRRequestHandler requestHandler = new DEHRRequestHandler(getPrivateKey());
                try {
//                    Date date= new Date();
//                    long time = date.getTime();
//                    final Timestamp ts = new Timestamp(time);
                    final long ts = Addressing.getCurrentTimestamp();
//                    Random rand = new Random();
//                    final int n = rand.nextInt(50);
                    final String name = "PatientName";
                    final String surname = "PatientSurname";
                    byte[] patientBody = requestHandler.addPatient(name + ts, surname + ts).toByteArray();
                    RequestBody body = RequestBody.create(MediaType.parse("application/octet-stream"), patientBody);

                    SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
                    String url = prefs.getString(PARAM_NAME_URL, DEHR_REST_API_DEFAULT);
                    Log.d("ADD_PATIENT", url);
                    String urlSuff = "/batches";
                    Request request = new Request.Builder()
                            .url(url + urlSuff)
                            .post(body)
                            .build();

                    client.newCall(request).enqueue(new Callback() {

                        @Override
                        public void onFailure(@Nullable Call call, @Nullable IOException e) {
                            if (e != null) {
                                e.printStackTrace();
                            }
                            final String myError = (e != null)?e.getMessage():"Null value";
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    mTextViewResult.setText(myError);
                                    Toast.makeText(MainActivity.this, myError, Toast.LENGTH_SHORT).show();
                                }
                            });
                        }

                        @Override
                        public void onResponse(@Nullable Call call, @Nullable Response response) throws IOException {
                            final String myResponse = (response != null && response.body() != null) ? response.body().string() : "Null value";
                            Log.d("ADD_PATIENT", myResponse);
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    SharedPreferences.Editor editor = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE).edit();
                                    String publicKey = getPublicKey(getPrivateKey());
                                    editor.putString(PARAM_NAME_PATIENT_PKEY, publicKey);
                                    editor.apply();
                                    Log.d("ADD_PATIENT", publicKey);
                                    mTextViewResult.setText(myResponse);
                                    String msg = "Patient registration: Name->" + name + ", Surname->" + surname + " sent";
                                    Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                                }
                            });
                        }
                    });
                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
        });
        //Grant access
        mButtonGrantAccess.setOnClickListener(new View.OnClickListener() {

            private void grantAccess(String doctorPKey) {
                OkHttpClient client = new OkHttpClient();

                DEHRRequestHandler requestHandler = new DEHRRequestHandler(getPrivateKey());
                try {
                    byte[] grantAccessBody = requestHandler.grantAccess(doctorPKey).toByteArray();
                    RequestBody body = RequestBody.create(MediaType.parse("application/octet-stream"), grantAccessBody);

                    SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
                    String url = prefs.getString(PARAM_NAME_URL, DEHR_REST_API_DEFAULT);
                    Log.d("GRANT_ACCESS", url);
                    String urlSuff = "/batches";
                    Request request = new Request.Builder()
                            .url(url + urlSuff)
                            .post(body)
                            .build();

                    client.newCall(request).enqueue(new Callback() {

                        @Override
                        public void onFailure(@Nullable Call call, @Nullable IOException e) {
                            if (e != null) {
                                e.printStackTrace();
                            }
                            final String myError = (e != null)?e.getMessage():"Null value";
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    mTextViewResult.setText(myError);
                                    Toast.makeText(MainActivity.this, myError, Toast.LENGTH_SHORT).show();
                                }
                            });
                        }

                        @Override
                        public void onResponse(@Nullable Call call, @Nullable Response response) throws IOException {
                            final String myResponse = (response != null && response.body() != null) ? response.body().string() : "Null value";
                            Log.d("GRANT_ACCESS", myResponse);
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    mTextViewResult.setText(myResponse);
                                    String msg = "Grant access sent";
                                    Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                                }
                            });
                        }
                    });
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void onClick(View view) {
                SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
                String doctorPKey = prefs.getString(PARAM_NAME_DOCTOR_PKEY, null);
                if(doctorPKey != null){
                    grantAccess(doctorPKey);
                } else {
                    Toast.makeText(MainActivity.this, "Doctor pkey not specified - scan QA code first", Toast.LENGTH_SHORT).show();
                }
            }
        });
        //Revoke access
        mButtonRevokeAccess.setOnClickListener(new View.OnClickListener() {

            private void revokeAccess(String doctorPkey) {
                OkHttpClient client = new OkHttpClient();

                DEHRRequestHandler requestHandler = new DEHRRequestHandler(getPrivateKey());
                try {
                    byte[] revokeAccessBody = requestHandler.revokeAccess(doctorPkey).toByteArray();
                    RequestBody body = RequestBody.create(MediaType.parse("application/octet-stream"), revokeAccessBody);

                    SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
                    String url = prefs.getString(PARAM_NAME_URL, DEHR_REST_API_DEFAULT);
                    Log.d("REVOKE_ACCESS", url);
                    String urlSuff = "/batches";
                    Request request = new Request.Builder()
                            .url(url + urlSuff)
                            .post(body)
                            .build();

                    client.newCall(request).enqueue(new Callback() {

                        @Override
                        public void onFailure(@Nullable Call call, @Nullable IOException e) {
                            if (e != null) {
                                e.printStackTrace();
                            }
                            final String myError = (e != null)?e.getMessage():"Null value";
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    mTextViewResult.setText(myError);
                                    Toast.makeText(MainActivity.this, myError, Toast.LENGTH_SHORT).show();
                                }
                            });
                        }

                        @Override
                        public void onResponse(@Nullable Call call, @Nullable Response response) throws IOException {
                            final String myResponse = (response != null && response.body() != null) ? response.body().string() : "Null value";
                            Log.d("REVOKE_ACCESS", myResponse);
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    mTextViewResult.setText(myResponse);
                                    String msg = "Revoke access sent";
                                    Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                                }
                            });
                        }
                    });
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void onClick(View view) {
                SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
                String doctorPKey = prefs.getString(PARAM_NAME_DOCTOR_PKEY, null);
                if(doctorPKey != null){
                    revokeAccess(doctorPKey);
                } else {
                    Toast.makeText(MainActivity.this, "Doctor pkey not specified - scan QA code first", Toast.LENGTH_SHORT).show();
                }
            }
        });
//        navView.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);
    }

    private void init() {
//        SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
//        String prKey = prefs.getString(DEHR_PRIVATE_KEY, null);
//        if(prKey == null){
//            prKey = generatePrivateKey();
//            SharedPreferences.Editor editor = prefs.edit();
//            editor.putString(DEHR_PRIVATE_KEY, prKey);
//            editor.apply();
//        }
        getPublicKey(getPrivateKey());

//        prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
//        String pubKey = prefs.getString(DEHR_PUBLIC_KEY, null);
//        if(pubKey == null){
//            PrivateKey prKeyObj = Secp256k1PrivateKey.fromHex(prKey);
//            pubKey = generatePublicKey(prKeyObj);
//            SharedPreferences.Editor editor = prefs.edit();
//            editor.putString(DEHR_PUBLIC_KEY, pubKey);
//            editor.apply();
//        }

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        // Check that it is the SecondActivity with an OK result
        if (requestCode == MY_CAMERA_REQUEST_CODE) {
            if (resultCode == RESULT_OK) {

                // Get String data from Intent
                String returnString = data.getStringExtra(QR_CODE_ENTERED_VALUE);
                Log.d("SCAN_QR_CODE", returnString != null? returnString:"Null value");
                SharedPreferences.Editor editor = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE).edit();
                editor.putString(PARAM_NAME_DOCTOR_PKEY, returnString);
                editor.apply();
                initDoctorPKeyValue();
                Toast.makeText(MainActivity.this, returnString, Toast.LENGTH_SHORT).show();
            }
        }
    }

    void initDoctorPKeyValue(){
        SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
        String pubKey = prefs.getString(PARAM_NAME_DOCTOR_PKEY, null);
        mTextDoctorPKey.setText(pubKey == null?"":pubKey);
    }

    private String getPublicKey(PrivateKey privateKey){
        SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
        String pubKey = prefs.getString(DEHR_PUBLIC_KEY, null);
        if(pubKey == null){
            pubKey = generatePublicKey(privateKey);
            SharedPreferences.Editor editor = prefs.edit();
            editor.putString(DEHR_PUBLIC_KEY, pubKey);
            editor.apply();
        }
        return pubKey;
    }

    private Secp256k1PrivateKey getPrivateKey(){
        SharedPreferences prefs = getSharedPreferences(DEHR_PREFS_NAME, MODE_PRIVATE);
        String prKey = prefs.getString(DEHR_PRIVATE_KEY, null);
        if(prKey == null){
            prKey = generatePrivateKey();
            SharedPreferences.Editor editor = prefs.edit();
            editor.putString(DEHR_PRIVATE_KEY, prKey);
            editor.apply();
        }
        return Secp256k1PrivateKey.fromHex(prKey);
    }

    private String generatePrivateKey() {
        Secp256k1Context context = new Secp256k1Context();
        return context.newRandomPrivateKey().hex();
    }

    private String generatePublicKey(PrivateKey privateKey){
        Secp256k1Context context = new Secp256k1Context();
        return context.getPublicKey(privateKey).hex();
    }

    @Override
    protected void attachBaseContext(Context newBase) {
        super.attachBaseContext(newBase);
        MultiDex.install(this);
    }

}
