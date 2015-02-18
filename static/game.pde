// Todo - REFACTOR TO REMOVE ALL MAGIC NUMBERS

interface Javascript {
  void yesCalled();
  void noCalled();
}

Javascript javascript;

void bindJavascript(Javascript js) {
  javascript = js;
}

boolean loading = true;
boolean gameOver = false;

void setLoading(boolean bool) {
  loading = bool;
}

void setGameOver(boolean bool) {
  gameOver = bool;
}

Paper paper;

void showPaper() {
  paper.setShowing(true);
}

void hidePaper() {
  paper.setShowing(false);
}

void setQuestion(String question) {
  paper.setQuestion(question);
}

// Setup the Processing Canvas
void setup(){
  size( 1000, 500 );
  frameRate(60);
  paper = new Paper();
}

// Main draw loop
void draw(){
  background( 0, 121, 184 );
  paper.draw();
  if (loading) {
    fill(0);
    textSize(70);
    text("Loading...", width / 2 - 100, height / 2)
  }
  if (gameOver) {
    fill(0);
    textSize(70);
    text("GAME OVER", width / 2 - 200, height / 2)
  }
}

void mousePressed() {
  if (mouseY >= paper.getY()){
    paper.clicked(mouseX, mouseY);
  }
 }

abstract class Drawable {
  int x, y;

  Drawable(int x, int y) {
    this.x = x;
    this.y = y;
  }

  int getX() {
    return this.x;
  }

  int getY() {
    return this.y;
  }

  void moveY(int y) {
    this.y -= y;
  }

  abstract void draw();
}

class Paper extends Drawable {

  String question = "Test Question";
  boolean showing = false;
  List<HolePunch> holepunches = new ArrayList<HolePunch>();
  ResponseBox yesBox = new ResponseBox(200, (500 + 200) - 100, "YES");
  ResponseBox noBox = new ResponseBox(1000 - 200, (500 + 200) - 100, "NO");

  Paper() {
    super(0, height);
  }

  void setShowing(boolean bool) {
    if(!showing && bool) {
      holepunches = new ArrayList<HolePunch>();
    }
    showing = bool;
  }

  void setQuestion(String question) {
    this.question = question;
  }

  void clicked(int x, int y) {
    holepunches.add(new HolePunch(x, y));

    // Check to see if yes or no was clicked
    // check yes
    if (x > yesBox.getX() && x < yesBox.getX() + 80 && y > yesBox.getY() &&  y < yesBox.getY() + 80) {
      hidePaper();
      if (javascript != null) {
        javascript.yesCalled();
      }
    }

    // check no
    if (x > noBox.getX() && x < noBox.getX() + 80 && y > noBox.getY() &&  y < noBox.getY() + 80) {
      hidePaper();
      if (javascript != null) {
        javascript.noCalled();
      }
    }
  }

  void move(u) {
      if (showing && y > height - 190) {
        y -= u;
        for (hole : holepunches) {
          hole.moveY(u);
        }
        yesBox.moveY(u);
        noBox.moveY(u);
      } else if (!showing && y < height ){
        y += u;
        for (hole : holepunches) {
          hole.moveY(-u);
        }
        yesBox.moveY(-u);
        noBox.moveY(-u);
      }
  }

  void draw() {
    move(15);

    stroke(255);
    strokeWeight(1);
    fill(240);
    rect(0, y, 1000, 200, 10);

    fill(20);
    textSize(30);
    text(question, 30, y + 70);
    yesBox.draw();
    noBox.draw();

    for (hole : holepunches) {
      hole.draw();
    }
  }
}

class ResponseBox extends Drawable {
  String response;

  ResponseBox (int x, int y, String resp) {
    super(x, y);
    this.response = resp;
  }

  void draw() {
    fill ( 255, 0, 0, 0);
    stroke(255, 0, 0);
    strokeWeight(3);
    rect(x, y, 80, 80);

    fill (255, 0, 0);
    textSize(50);
    text(response, x - 120, y + 50)
  }
}

class HolePunch extends Drawable {
  Chad chad;

  HolePunch (int x, int y) {
    super(x, y);
    chad = new Chad(x, y);
  }

  void draw() {
    stroke(255, 0,0,0)
    fill(0, 121, 184);
    ellipse(x, y, 20, 20);

    chad.draw();
  }
}

class Chad extends Drawable {
  int velX, velY;
  double gravity = 2.5;


  Chad (int x, int y) {
    super(x, y);
    velX = random(-25, 25);
    velY = random(-25, 0)
  }

  void update() {
    velY += gravity;
    x -= velX;
    y += velY;
  }

  void draw() {
    update()

    stroke(0);
    strokeWeight(.4);
    fill(240);
    ellipse(x, y, 20, 20);
  }
}