import beads.*;
import java.net.*;
import java.io.*;
import javax.sound.sampled.AudioFormat;

AudioContext ac;

UGen mic;
Gain inputGain;
AmbienceProcessor ambProc;
SoundInjector injector;
SentientReceiver emotionListener;
SampleRecorder recorder;

ArrayList<Sample> samples;

boolean fakeEmotion = false;

boolean injecting = false;

void setup()
{
  size(500, 500);
  frameRate(30);
  
  emotionListener = new SentientReceiver("128.122.151.163", "JRoom-2013-11-24-22-51-01");
  emotionListener.start();
  
  ac = new AudioContext();
  
  mic = ac.getAudioInput();
  // the mic input gain is silent, we only listen to the mic
  inputGain = new Gain(ac, 1, 0);
  inputGain.addInput(mic);
  ac.out.addInput(inputGain);
  
  injector = new SoundInjector(ac);
  ambProc = new AmbienceProcessor(ac, mic);

  samples = new ArrayList<Sample>();
  
  ac.start();
  ambProc.start();
  injector.start();
}

void draw()
{
  background(0);
  
  float amp = ambProc.getCurrentVolume();
  
  float rec = random(200);
  if (rec < 2)
  {
    if (amp > 0.1)
    {
      // record env samples
      if (recorder == null)
      {
        if (amp > 0.1)
        {
          println("recording sample");
          long length = 5000 + (long)random(2000);
          recorder = new SampleRecorder(ac, mic, length);
          recorder.start();
          injector.recordSample(length);
        }
      }      
    }
  }
  
  /* handle system emotions and trigger sounds accordingly */
  if (emotionListener.getCurrentEmotion().equals("Nervous")) 
  { 
    if (amp > 0.2) {
      injector.playWind();
    }
  }
  else if (emotionListener.getCurrentEmotion().equals("Agitated")) 
  { 
    if (amp > 0.2) {
      injector.playShh();
    }  
  }
  else if (emotionListener.getCurrentEmotion().equals("Overwhelmed")) 
  { 
    int r = (int)random(100);

    if (r<10) {
      // random (30-40): play prerecorded samples
      if (amp > 0.1)
      {
        if (samples.size() > 0)
        {
          int sIndex = (int)random(samples.size());
          {
            injector.playSample(samples.get(sIndex));
          }
        }
      }
    }
    else if (r < 30) {
      // random (40-100): play shh noise
      if (amp > 0.1) {
        injector.playShh();
      }
    }
  }
  
  // check for finished recording samples
  if (recorder != null) {
    if (recorder.finished) {
      samples.add(recorder.getSample());
      recorder = null;
    }
  }

  ambProc.draw(0, height/2+10, width, height/2-20);
  
  drawWaveForm(0, 0, width, height/2);
}

void drawWaveForm(int x, int y, int w, int h)
{
  noFill();
  stroke(255);
  rect(x, y, w, h);
  
  loadPixels();
  //set the background
  //scan across the pixels
  for(int i = 0; i < w; i++)
  {
    // for each pixel, work out where in the current audio
    // buffer we are
    int buffIndex = i * ac.getBufferSize() / w;
    // then work out the pixel height of the audio data at
    // that point
    int vOffset = (int)((1 + mic.getValue(0, buffIndex)) *
                  h / 2);
    //draw into Processing's convenient 1-D array of pixels
    pixels[y*width + x + vOffset * height + i] = color(255);
  }
  // paint the new pixel array to the screen
  updatePixels();
}

float getMaxAmplitude()
{
  float max=-1000;
  
  for (int i=0; i<ac.getBufferSize(); i++)
  {
    float val = mic.getValue(0, i);
    if (abs(val) > max) {
      max = abs(val);
    }
  }
  
  return max;
}

public void keyPressed()
{
  println(keyCode);
  if (keyCode == 82)  // 'r'
  {
    if (recorder == null)
    {
      println("recording sample");
      long length = 5000 + (long)random(2000);
      recorder = new SampleRecorder(ac, mic, length);
      recorder.start();
      injector.recordSample(length);
    }
  }
  else if (keyCode == 80) // 'p'
  {
    if (samples.size() > 0)
    {
      int sIndex = (int)random(samples.size());
      {
        injector.playSample(samples.get(sIndex));
      }
    }
  }
}

