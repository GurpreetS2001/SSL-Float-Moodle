
#include <FL/Fl.H> // needed in every fltk program
#include <FL/Fl_Window.H> // needed to use the Fl_Window class
#include <FL/Fl_Button.H> // needed to use the Fl_Box class
#include <FL/Fl_Radio_Button.H> // needed to use the Fl_Box class
#include <FL/Fl_Light_Button.H> // needed to use the Fl_Box class

int main(int argc, char *argv[]) {
    	Fl_Window *window;

window = new Fl_Window (600,600,"DEMO"); // outer window

        Fl_Button *button1 = new Fl_Button(100,100,100,100,"Box 1!");

	//window->color(FL_WHITE);
	//button1->down_color(FL_RED);
	button1->label("10");

    	window->end();
    	window->show();
    	return(Fl::run());  // the process waits from here on for events
}


