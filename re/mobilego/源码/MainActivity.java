package com.example.mobilego;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import game.Game;
public class MainActivity extends AppCompatActivity {
    private Button button;
    private EditText editText;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        editText=(EditText) findViewById(R.id.editText);
        button=(Button) findViewById(R.id.button);
        button.setOnClickListener((View v)-> {
            if (Game.checkflag(editText.getText().toString()).equals(getResources().getString(R.string.cmp))) {
                Toast.makeText(this, "yes your flag is right", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "No No No", Toast.LENGTH_SHORT).show();
            }
        }
       );
    }
}