
class SampleRecorder extends Thread
{
  Sample sample;
  RecordToSample rts;
  UGen mic;
  AudioContext ac;
  long length;
  boolean finished;
  
  public SampleRecorder(AudioContext ac, UGen mic, long l)
  {
    this.ac = ac;
    this.mic = mic;
    length = l;
    
    finished = false;
    
    // setup the recording
    try {
      AudioFormat af = new AudioFormat(44100f, 16, 1, true, true);
      sample = new Sample(af, 44100);
      rts = new RecordToSample(ac, sample, RecordToSample.Mode.INFINITE);
      rts.pause(true);
    }
    catch (Exception e) {
      println("error initializing sample recorder");
    }
    
    rts.addInput(mic);
    ac.out.addDependent(rts);
    
  }
  
  public void run()
  {
    rts.start();
    try {
      Thread.sleep(length);
    }
    catch (Exception e) {}
    
    rts.pause(true);
    finished = true;
  }
  
  public Sample getSample()
  {
    return sample;
  }
  
}
