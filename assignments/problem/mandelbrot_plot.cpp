#include <SDL2/SDL.h>
#include <string>
#include <tuple>
#include <iostream>
#include <time.h>

//------- IMPORTANT CONSTANTS ------------

//SCREEN ASPECT
int WIDTH = 500;
int HEIGHT = 500;


//COORDINATE FRAME ASPECT
long double min = -2.84;
long double max = 1.0;

//INITIAL BOUND FOR STABILITY CHECK
int MAX_ITERATIONS = 500;
long double factor = 1;

//MAX ZOOM IN EITHER + OR - DIRECTION
int MAX_LAYERS = 50;



//----------- STRUCTS/CLASSES IMPLEMENTING IDEATED DATA STRUCTURE ------------------ 

//(stores necessary data to improve efficiency of code and avoid repetitive calculation)
//decreases time complexity at the expense space/memory usage

//STRUCT RERESENTS EACH COLOURED 'BOX' OR 'PIXEL' ON THE SCREEN
struct Pixel{

    //coordinate
    int x_1;
    int y_1;

    //colour
    std::tuple<int,int,int>rgb1;

    //constructor
    Pixel(int x, int y, std::tuple<int,int,int>rgb){
        x_1 = x;
        y_1 = y;
        rgb1 = rgb;
    }
};

//CLASS WHICH WILL REPRESENT THE SCREEN AT A PARTICULAR ZOOM VALUE-- acts as a collection of pixels
class Layer{

    Pixel **array; //array of pixel pointers
    int zoom; //zoom value of thus layer

    public:
    //member functions

    Layer(int iterations); //constructor
    void add_pixel(int x, int y, std::tuple<int,int,int>rgb); //add new pixel data to this layer
    void display_layer(SDL_Renderer** renderer1); //display stored layer
};

//function definitions
Layer::Layer(int iterations){ 
    //initialises new layer
        array = new Pixel *[WIDTH*HEIGHT];
        zoom = (iterations-500)/10;
}

void Layer::add_pixel(int x, int y, std::tuple<int,int,int>rgb){
    //creates pixel corresponding to provided data and stores pointer to it
        Pixel *pixel=new Pixel(x,y,rgb);
    //function to map x,y to array index
        array[500*y+x]=pixel;
}

void Layer::display_layer(SDL_Renderer** renderer1){
    //colour the screen according to previously saved data
        for(int i=0; i<WIDTH*HEIGHT; i++){
            SDL_SetRenderDrawColor(*renderer1, std::get<0>(array[i]->rgb1), std::get<1>(array[i]->rgb1), std::get<2>(array[i]->rgb1), 255);
            SDL_RenderDrawPoint(*renderer1,array[i]->x_1,array[i]->y_1);
        }
}


//function mapping a given value wrt one range to a new value wrt new boundaries
long double map(long double value,long double in_min,long double in_max,long double out_min,long double out_max){
    return (value - in_min)*(out_max-out_min)/(in_max-in_min)+out_min;
}


//---------------COLOURING ALGORITHM---------------

//takes number of iterations a point took to escape |2| and maps the corresponding 'stability' values to r-g-b values
//returns rgb values as a tuple of intergers (r,g,b)
//in general, for a particular shade among r,g,b: darker shade corresponds to less stability

std::tuple<int,int,int> get_colour(int break_number){

    //COLOURING 1:

    int stability = map(break_number, 0, MAX_ITERATIONS, 0, 255);
    //black will be the most stable
    int r = 0;
    int g = 0;
    int b = 0;
    if(stability>=15){
        //blue means high stability
        b = map(sqrt(sqrt(stability)), 0, sqrt(sqrt(255)), 0, 255);
    }
    else if(stability>=5){
        //green lies in-between wrt stability
        g = map(sqrt(sqrt(stability)),0,sqrt(sqrt(255)),35,255);
    }
    else if(stability>0){
        //red signifies least stable
        r = map(sqrt(sqrt(stability)),0,sqrt(sqrt(255)),50,255);
    }
    return (std::make_tuple(r,g,b));

    /* -------------------------

    COLOURING 2:

    int stability = map(break_number, 0, MAX_ITERATIONS, 0, 255);
    int r = 0;
    int g = 0;
    int b = 0;
    if(break_number>=5){
        b = map(sqrt(sqrt(stability)), 0, sqrt(sqrt(255)), 0, 255);
    }
    if(break_number<5 && break_number>=2){
        g = map(sqrt(sqrt(stability)),0,sqrt(sqrt(255)),50,255);
    }
    if(break_number<2 && break_number>0){
        r = map(sqrt(sqrt(stability)),0,sqrt(sqrt(255)),100,255);
    }


    ---------------------------
    COLOURING 3:
    
    double stability = break_number/MAX_ITERATIONS;
    double r,g,b;
    if(stability==0){r=0;g=0;b=0;}
    else if(stability<0.33){r=stability*255; g=255; b=255;}
    else if(stability<0.66){g=stability*255; r=255; b=255;}
    else{b=stability*255;g=0;r=0;}
    */
}


//------------- ESCAPE TIME ALGORITHM --------------

//for point x+iy; this computes and returns the max number of iterations for which z^2 + c stays within |2|
//if number of iterations reaches MAX_ITERATIONS without value becoming greator that |2|, we deem the point stable

int get_break_value(long double *x, long double *y){

    int iterations = 0;

    //imaginary and real parts handles separately
    long double initial_x = *x;
    long double initial_y = *y;

    //repeating application of function z^2 + c for z = 0 at c = x + iy.
    for(int i = 0; i< MAX_ITERATIONS; i++){

        //computing z^2 + c
        long double dummy_x = *x*(*x) - *y*(*y);
        long double dummy_y = 2*(*x)*(*y);
                                    
        *x = dummy_x + initial_x;
        *y = dummy_y + initial_y;

        //checking if value has escaped |2| and exiting loop if true
        if(sqrt(*x*(*x) + *y*(*y)) > 2){
            break;
        }

        iterations++;
        }

    //return break value
    return iterations;
}


//--------------- MAIN --------------------------

int main(int argc,char* argv[]){

    //SDL initialization for window and renderer
    SDL_Init(SDL_INIT_EVERYTHING);

    SDL_Window* window;
    SDL_Renderer* renderer;
    SDL_CreateWindowAndRenderer(900,900,0,&window,&renderer);
    SDL_RenderSetLogicalSize(renderer,WIDTH,HEIGHT);


    //enables tracking real time input
    SDL_Event event;
    
    //clock_t variables to track time taken for rendering each layer/frame
    clock_t start,end;
    double time_taken;

    //variables necessary to track current layer on screen
    long double prev_max;
    int current_zoom;
    Layer *current_layer;

    //arrays of pointers to previously computed layers
    Layer **zoomed_in_layers = new Layer *[MAX_LAYERS];
    Layer **zoomed_out_layers = new Layer *[MAX_LAYERS];

    //initialising all pointers to NULL
    for(int i=0; i<MAX_LAYERS; i++){
        zoomed_in_layers[i] = NULL;
        zoomed_out_layers[i] = NULL;
    }

// WINDOW BEGINS RENDERING AND ACCEPTING REAL TIME INPUT
while (max>min){

// FOR INTERACTIVE ZOOM:

    while (SDL_PollEvent(&event) ){
    switch (event.type)
    {
        //handles closing of window
        case SDL_QUIT: return 1;
        
        //handles mouse click
        case SDL_MOUSEBUTTONUP:
                //ZOOM IN
                factor *= 0.9349;
                max-=0.1*factor;
                min+=0.14*factor; 
                MAX_ITERATIONS+=10;         
            break;

        //handles keyboard button press
        case SDL_KEYUP:
                //ZOOM OUT
                factor /= 0.9349;  
                max+=0.1*factor;
                min-=0.14*factor;
                MAX_ITERATIONS-=10;                
            break;
    } 
    }

/* 
     FOR ZOOM IN ANIMATION:
        
        if(factor>0.1){
            factor *= 0.9349;
            MAX_ITERATIONS+=20;
            max-=0.12*factor;
            min+=0.15*factor;
        }
        else if(factor>0.025){
            max-=0.1*factor;
            min+=0.14*factor;
            factor *= 0.934;
            MAX_ITERATIONS+=5;
        }
        else{
            max-=0.1*factor;
            min+=0.08*factor;
            factor*=0.99;
        }

*/

    //RENDERING CURRENT LAYER
        if(max!=prev_max){
        prev_max=max; //updating variable that tracks current max_x value

        //layer zoom
        current_zoom=(MAX_ITERATIONS-500)/10;  


        if(current_zoom!=0){
            //displayimg parameters
            std::cout<<"------- LAYER ZOOM: "<<current_zoom<<" -------"<<std::endl;
            std::cout<<"x-limits of screen: ["<<min<<", "<<max<<"]"<<std::endl;
            std::cout<<"y-limits of screen: ["<<min+1<<", "<<max+1<<"]"<<std::endl;
            std::cout<<"Number of iterations for stability check: "<<MAX_ITERATIONS<<std::endl;    
        }

        SDL_RenderPresent(renderer);

        //start tracking time
        start=clock(); 

        if((current_zoom>=0 && zoomed_in_layers[current_zoom]==NULL)||(current_zoom<=0&&zoomed_out_layers[-current_zoom]==NULL)){
            //if the current zoom value layer has never been computed before we enter this block

            //creates the new layer object
            //stores pointer in zoomed in or out

            if(current_zoom>0){
                //xoomed in
                current_layer = new Layer(MAX_ITERATIONS);
                zoomed_in_layers[current_zoom]=current_layer;
            }

            else if(current_zoom<0){
                //zoomed out
                current_layer = new Layer(MAX_ITERATIONS);
                zoomed_out_layers[-current_zoom]=current_layer;
            }

            else{
                //0-zoom layer in both arrays
                current_layer = new Layer(MAX_ITERATIONS);
                zoomed_in_layers[0]=current_layer;
                zoomed_out_layers[0]=current_layer;
            }


            //uterating over points/pixels in window dimensioned-coordinates
            for(int x = 0; x<WIDTH ; x++){
                for(int y=0; y<HEIGHT ; y++){

                //mapping window dimensions to desired complex plane section
                long double x_cord = map(x, 0, WIDTH, min, max);
                long double y_cord = map(y, 0,HEIGHT, min+1, max+1);

                //calling our escape time algorithm function 
                //returns the number of iterations of function z^c + c for z=0, c = x+iy after which it escapes |2|
                int break_iterations = get_break_value(&x_cord,&y_cord);                


                if(break_iterations == MAX_ITERATIONS){
                    //black colour for the most stable numbers points
                    std::tuple<int,int,int> rgb = get_colour(0);

                    //renders plot with obtained (r,g,b) values
                    SDL_SetRenderDrawColor(renderer, std::get<0>(rgb), std::get<1>(rgb), std::get<2>(rgb), 255);
                    SDL_RenderDrawPoint(renderer,x,y);

                    //adds pixel to our layer object
                    current_layer->add_pixel(x,y,rgb); 
                }

                else{
                    //calls our get_colour function which implements break iteration->stability->colour mapping
                    std::tuple<int,int,int> rgb = get_colour(break_iterations);

                    //renders plot with obtained (r,g,b) values
                    SDL_SetRenderDrawColor(renderer, std::get<0>(rgb), std::get<1>(rgb), std::get<2>(rgb), 255);
                    SDL_RenderDrawPoint(renderer,x,y);

                    //adds pixel to our layer object
                    current_layer->add_pixel(x,y,rgb);
                }
                }
            }
        //control exits new-layer computation operations block
        }

        else{
            //if the current_layer has already been computed, its will be stored in the zoomed in or out arrays
            //in that case, we do not need to run through the algorithms again, 
            //we simply render plot by extracting values stored in our layer object using the display_layer member function
            if(current_zoom>=0){zoomed_in_layers[current_zoom]->display_layer(&renderer);}
            else{zoomed_out_layers[-current_zoom]->display_layer(&renderer);}
        }
       
        end=clock(); 
        //render end-time noted

        //time taken in current layer render in secinds
        time_taken = double(end - start) / double(CLOCKS_PER_SEC);

        //display
            if(current_zoom!=0){
                std::cout<<"Time taken to load frame (in secs): "<<time_taken<<std::endl;
            }
        }

    //CONTROL EXITS NEW RENDER BLOCK        
    }

}
//------------------------- END ----------------------------
    