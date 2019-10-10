package com.medicalinsurance;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.google.android.material.snackbar.Snackbar;
import com.google.zxing.BarcodeFormat;
import com.google.zxing.Result;

import java.util.ArrayList;
import java.util.List;

import me.dm7.barcodescanner.zxing.ZXingScannerView;
import me.dm7.barcodescanner.zxing.ZXingScannerView.ResultHandler;

import static com.medicalinsurance.MainActivity.MY_CAMERA_REQUEST_CODE;
import static com.medicalinsurance.MainActivity.QR_CODE_ENTERED_VALUE;

public class ScanQrCodeActivity extends AppCompatActivity implements ResultHandler{

    static final String HUAWEI = "huawei";

    private ZXingScannerView qrCodeScanner;
    private RelativeLayout scanQrCodeRootView;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_scan_qr_code);
        qrCodeScanner = findViewById(R.id.qrCodeScanner);
        setScannerProperties();
        scanQrCodeRootView = findViewById(R.id.scanQrCodeRootView);
        ImageView barcodeBackImageView = findViewById(R.id.barcodeBackImageView);
        barcodeBackImageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onBackPressed();
            }
        });

    }

    @Override
    public void handleResult(Result result) {
        Intent intent = new Intent();
        intent.putExtra(QR_CODE_ENTERED_VALUE, result.getText());
        setResult(RESULT_OK, intent);
        finish();
        resumeCamera();
    }


    @Override
    protected void onResume() {
        super.onResume();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA},
                        MY_CAMERA_REQUEST_CODE);
            }
        }
        qrCodeScanner.startCamera();
        qrCodeScanner.setResultHandler(this);
    }

    @Override
    protected void onPause() {
        super.onPause();
        qrCodeScanner.stopCamera();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == MY_CAMERA_REQUEST_CODE) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED)
                openCamera();
            else if (grantResults[0] == PackageManager.PERMISSION_DENIED)
                showCameraSnackBar();
        }
    }

    private void resumeCamera() {
//        Toast.LENGTH_LONG;
//        val handler = Handler()
//        handler.postDelayed({  }, 2000);
        final Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                qrCodeScanner.resumeCameraPreview(ScanQrCodeActivity.this);
            }
        }, 2000);
    }

    private void openCamera() {
        qrCodeScanner.startCamera();
        qrCodeScanner.setResultHandler(this);
    }

    private void showCameraSnackBar() {
        if (ActivityCompat.shouldShowRequestPermissionRationale(this, Manifest.permission.CAMERA)) {
            Snackbar snackbar = Snackbar.make(scanQrCodeRootView, this.getString(R.string.app_needs_your_camera_permission_in_order_to_scan_qr_code), Snackbar.LENGTH_LONG);
            View view1 = snackbar.getView();
            view1.setBackgroundColor(ContextCompat.getColor(this, R.color.whiteColor));
            TextView textView = view1.findViewById(com.google.android.material.R.id.snackbar_text);
            textView.setTextColor(ContextCompat.getColor(this, R.color.colorPrimary));
            snackbar.show();
        }
    }

    private void setScannerProperties() {
        List<BarcodeFormat> list = new ArrayList<>();
        list.add(BarcodeFormat.QR_CODE);
        qrCodeScanner.setFormats(list);
        qrCodeScanner.setAutoFocus(true);
        qrCodeScanner.setLaserColor(R.color.colorAccent);
        qrCodeScanner.setMaskColor(R.color.colorAccent);
        if (Build.MANUFACTURER.equalsIgnoreCase(HUAWEI)){
            qrCodeScanner.setAspectTolerance(0.5f);
        }

    }

}