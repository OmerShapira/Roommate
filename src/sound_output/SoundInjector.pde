class SoundInjector extends Thread
{
  AudioContext ac;
  ArrayList<InjectorMessage> msgs;
  
  boolean isRunning;
  
  public SoundInjector(AudioContext ac)
  {
    this.ac = ac;
    msgs = new ArrayList<InjectorMessage>();
  }
  
  public void curtainRandom()
  {
    msgs.add(new InjectorMessage(InjectorTask.CURTAIN_RANDOM, System.currentTimeMillis()));
  }
  
  public void curtainOpen()
  {
    msgs.add(new InjectorMessage(InjectorTask.CURTAIN_OPEN, System.currentTimeMillis()));
  }  

  public void curtainClose()
  {
    msgs.add(new InjectorMessage(InjectorTask.CURTAIN_CLOSE, System.currentTimeMillis()));
  }  
  
  public void recordSample(long length)
  {
    injecting = true;
    ambProc.clearVol();
    msgs.add(new InjectorMessage(InjectorTask.REC_SAMPLE, System.currentTimeMillis()));
    msgs.add(new InjectorMessage(InjectorTask.STOPREC_SAMPLE, System.currentTimeMillis()+length));
  }
  
  public void playShh()
  {
    println("injecting shh");
    injecting = true;
    ambProc.clearVol();
    msgs.add(new InjectorMessage(InjectorTask.CURTAIN_OPEN, System.currentTimeMillis()));
    msgs.add(new InjectorMessage(InjectorTask.PLAY_SHH, System.currentTimeMillis()));
    msgs.add(new InjectorMessage(InjectorTask.CURTAIN_SHUT, System.currentTimeMillis()+10000));
    msgs.add(new InjectorMessage(InjectorTask.STOP_SHH, System.currentTimeMillis()+20000));
  }
  
  public void playWind()
  {
    println("injecting wind");
    injecting = true;
    ambProc.clearVol();
    msgs.add(new InjectorMessage(InjectorTask.PLAY_WIND, System.currentTimeMillis()));
    msgs.add(new InjectorMessage(InjectorTask.STOP_WIND, System.currentTimeMillis()+20000));
  }
  
  public void playSample(Sample s)
  {
    println("playing random sample");
    injecting = true;
    ambProc.clearVol();
    msgs.add(new InjectorMessage(InjectorTask.PLAY_SAMPLE, System.currentTimeMillis(), s));
    msgs.add(new InjectorMessage(InjectorTask.STOP_SAMPLE, System.currentTimeMillis() + (long)s.getLength()));
    
  }
    
  public void run()
  {
    isRunning = true;
    while (isRunning)
    {
      ArrayList<InjectorMessage> toDelete = new ArrayList<InjectorMessage>();
      
      long time = System.currentTimeMillis();
      for (int i=0; i<msgs.size() ;i++)
      {
        InjectorMessage msg = msgs.get(i);
        if (msg.time <= time) {
          // handle the message
          handleMessage(msg);
          
          // mark the message for deletion
          toDelete.add(msg);
        }
      }
      
      for (InjectorMessage msg : toDelete)
      {
        msgs.remove(msg);
      }

      try {      
        Thread.sleep(20);
      }
      catch (Exception e) {}
    }
  }
  
  public void handleMessage(InjectorMessage msg)
  {
    if (msg.task == InjectorTask.PLAY_SHH) {
      injectShh();
    }
    else if (msg.task == InjectorTask.STOP_SHH) {
      injecting = false;
    }        
    else if (msg.task == InjectorTask.PLAY_WIND) {
      injectWave();
    }
    else if (msg.task == InjectorTask.STOP_WIND) {
      injecting = false;
    }
    else if (msg.task == InjectorTask.PLAY_SAMPLE) {
      injectGranularSample(msg.sample);
//      injectSample(msg.sample);
    }
    else if (msg.task == InjectorTask.STOP_SAMPLE) {
      injecting = false;
    }
    else if (msg.task == InjectorTask.STOPREC_SAMPLE) {
      injecting = false;
    }
    else if (msg.task == InjectorTask.CURTAIN_RANDOM) {
      serialSend("2");
    }
    else if (msg.task == InjectorTask.CURTAIN_OPEN) {
      serialSend("8");
    }
    else if (msg.task == InjectorTask.CURTAIN_CLOSE) {
      serialSend("1");
    }
    else if (msg.task == InjectorTask.CURTAIN_SHUT) {
      serialSend("0");
    }
  }
  
  private void serialSend(String s)
  {
    if (useSerial) {
      serial.write(s);
    }
    else {
      println(s);
    }
  }
  
  private void injectSample(Sample s)
  {
    SamplePlayer sp = new SamplePlayer(ac, s);
    Envelope gainEnv = new Envelope(ac, 0.0);
    gainEnv.addSegment(1, 2000);
    gainEnv.addSegment(1, s.getLength()-1000);
    gainEnv.addSegment(0, s.getLength());
    Gain spGain = new Gain(ac, 1, gainEnv);
    spGain.addInput(sp);
    ac.out.addInput(spGain);
  }

  private void injectGranularSample(Sample s)
  {
    GranularSamplePlayer gsp = new GranularSamplePlayer(ac, s);
    Glide randomnessValue = new Glide(ac, 80, 10);
    
    Envelope intEnv = new Envelope(ac, 100);
    intEnv.addSegment(60, 2000);
    intEnv.addSegment(5, 200);
    intEnv.addSegment(5, 2000);
    intEnv.addSegment(100, 200);
//    Glide intervalValue = new Glide(ac, 5, 100);
    
    Envelope gsizeEnv = new Envelope(ac, 300);
    gsizeEnv.addSegment(5, 300);
    gsizeEnv.addSegment(10, 300);
    gsizeEnv.addSegment(50, 300);
    
    Envelope posEnv = new Envelope(ac, 0);
    posEnv.addSegment(s.getLength(), s.getLength());
//    Glide grainSizeValue = new Glide(ac, 50, 50);
//    Glide positionValue = new Glide(ac, random(0,s.getLength()-500), 30);
    Glide pitchValue = new Glide(ac, 1, 20);
    gsp.setRandomness(randomnessValue);
    gsp.setGrainInterval(intEnv);
    gsp.setGrainSize(gsizeEnv);
    gsp.setPosition(posEnv);
    gsp.setPitch(pitchValue);
    
//    Envelope gainEnv = new Envelope(ac, 0.0);
//    gainEnv.addSegment(1, 2000);
//    gainEnv.addSegment(1, s.getLength()-1000);
//    gainEnv.addSegment(0, s.getLength());
//    Gain gspGain = new Gain(ac, 1, gainEnv);
//    gspGain.addInput(gsp);
    ac.out.addInput(gsp);
    gsp.start();
  }
  
  private void injectShh()
  {
    Noise noise = new Noise(ac);
//    noise.pause(true);
    
    // setup low-pass filter
    Envelope filterEnv = new Envelope(ac, 0.0);
    filterEnv.addSegment(0.05, 5000);
    filterEnv.addSegment(900, 5000);
    filterEnv.addSegment(2000, 100);
    filterEnv.addSegment(2000, 1000);
    filterEnv.addSegment(900, 100);
    filterEnv.addSegment(0.0, 5000);
    LPRezFilter filter = new LPRezFilter(ac, filterEnv, 0.9);
    filter.addInput(noise); 
    
    // setup gain evelope
    Envelope gainEnv = new Envelope(ac, 0.0);
    gainEnv.addSegment(0.1, 5000);
    gainEnv.addSegment(0.6, 5000);
    gainEnv.addSegment(0.05, 5000);
    gainEnv.addSegment(0.05, 10000);
    gainEnv.addSegment(0.0, 10000);
    Gain gain = new Gain(ac, 1, gainEnv);
    gain.addInput(filter);
    
    ac.out.addInput(gain);
  }
  
  private void injectWave()
  {
    Noise noise = new Noise(ac);
//    noise.pause(true);
    
    // setup low-pass filter
    Envelope filterEnv = new Envelope(ac, 0.0);
    filterEnv.addSegment(0.05, 5000);
    filterEnv.addSegment(900, 5000);
    filterEnv.addSegment(900, 100);
    filterEnv.addSegment(0.0, 5000);
    LPRezFilter filter = new LPRezFilter(ac, filterEnv, 0.9);
    filter.addInput(noise); 
    
    // setup gain evelope
    Envelope gainEnv = new Envelope(ac, 0.0);
    gainEnv.addSegment(0.1, 5000);
    gainEnv.addSegment(0.8, 5000);
    gainEnv.addSegment(0.05, 5000);
    gainEnv.addSegment(0.05, 10000);
    gainEnv.addSegment(0.0, 2000);
    Gain gain = new Gain(ac, 1, gainEnv);
    gain.addInput(filter);
    
    ac.out.addInput(gain);
  }
  
}


class InjectorMessage
{
  long time;
  InjectorTask task;
  Sample sample;
  
  public InjectorMessage(InjectorTask task, long time)
  {
    this.task = task;
    this.time = time;
    sample = null;
  }
  
  public InjectorMessage(InjectorTask task, long time, Sample sample)
  {
    this.task = task;
    this.time = time;
    this.sample = sample;
  }
}


