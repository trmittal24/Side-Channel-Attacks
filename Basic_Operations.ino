int a, b, c,d,e, f;
  

void setup() {
  // put your setup code here, to run once:
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  Serial.begin(2000000);

  a = 87;
  b = 56;
  f = 31982;

}

void loop() {
  // put your main code here, to run repeatedly:
  PORTB |= 0x08;

  
  PORTB |= 0x10;
  c = (a*b);
  PORTB &= ~0x10;

  PORTB |= 0x10;
  d = c % f;
  PORTB &= ~0x10;

  PORTB |= 0x10;
  e = a + d;
  PORTB &= ~0x10;

  PORTB |= 0x10;
  f = e<< 1;
  PORTB &= ~0x10;  


  //Serial.println(c+d+e);
//  Serial.println(d);
//  Serial.println(e);
//  
  PORTB &= ~0x08;  

  
}
