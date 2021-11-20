#include<bits/stdc++.h>
using namespace std;

struct Cell{
    int num=0;
    int x=-1;
    int y=-1;
    bool visited=false;
    bool left=false;    //i=0
    bool up=false;      //i=1
    bool right=false;   //i=2
    bool down=false;    //i=3
    Cell(){};
    Cell(int x,int y,bool left,bool up,bool right,bool down){
        this->x=x;
        this->y=y;
        this->left=left;
        this->up=up;
        this->right=right;
        this->down=down;
    }
};

class Maze{
    queue<Cell*> cellStack;
    int rows;
    int cols;
    Cell** cell_array;
    int** row_walls;
    int** col_walls;
    public:
    Maze(int N,int M);
    void GetWalls();
    bool checkwall(int x,int y,int i);
    void SetCells();
    void BFS();
    void getShortestPath();
    void getMaze();
};

Maze::Maze(int N,int M){
    rows=N;
    cols=M;
    cell_array=new Cell*[N-1];
    for(int i=0;i<N-1;i++){
        cell_array[i]=new Cell[M-1];
    }
    row_walls=new int*[N];
    for(int i=0;i<N;i++){
        row_walls[i]=new int[M-1];
    }
    col_walls=new int*[M];
    for(int i=0;i<M;i++){
        col_walls[i]=new int[N-1];
    }
    GetWalls();
    SetCells();
    cellStack.push(&cell_array[0][0]);
    BFS();
}

void Maze::GetWalls(){
//get rows
cout<<"Input Row Walls\n";
for(int i=0;i<rows;i++){
    cout<<"Input row "<<i+1<<'\n';
    for(int j=0;j<cols-1;j++){
        cin>>row_walls[i][j];
    }
}
//get cols
cout<<"Input Col Walls\n";
for(int i=0;i<cols;i++){
    cout<<"Input cols "<<i+1<<'\n';
    for(int j=0;j<rows-1;j++){
        cin>>col_walls[i][j];
    }
}
}

void Maze::SetCells(){
    for(int i=0;i<rows-1;i++){
        for(int j=0;j<cols-1;j++){
            bool left=checkwall(i,j,0);
            bool up=checkwall(i,j,1);
            bool right=checkwall(i,j,2);
            bool down=checkwall(i,j,3);
            cell_array[i][j]=Cell(i,j,left,up,right,down);
        }
    }
}

bool Maze::checkwall(int x,int y,int i){
    if(i==0){
        if(col_walls[y][x]==1)return true;
        else return false;       
    }
    else if(i==1){
        if(row_walls[x][y]==1)return true;
        else return false;       
    }
    else if(i==2){
        if(col_walls[y+1][x]==1)return true;
        else return false;       
    }
    else if(i==3){
        if(row_walls[x+1][y]==1)return true;
        else return false;       
    }
    else{
        cout<<"checkwall function called incorrectly";
        return false;
    }
}

void Maze::BFS(){
    while(!cellStack.empty()){
        Cell* dum=cellStack.front();
        cellStack.pop();
        dum->visited=true;
        int level=dum->num;
        if(dum->left == false){
            if(dum->y-1>=0){
                if(!cell_array[dum->x][dum->y-1].visited){
                    cell_array[dum->x][dum->y-1].num=level+1;
                    cellStack.push(&cell_array[dum->x][dum->y-1]);
                }
            }
        }
        if(dum->up == false){
            if(dum->x-1>=0){
                if(!cell_array[dum->x-1][dum->y].visited){
                    cell_array[dum->x-1][dum->y].num=level+1;
                    cellStack.push(&cell_array[dum->x-1][dum->y]);
                }
            }
        }
        if(dum->right == false){
            if(dum->y+1<cols-1){
                if(!cell_array[dum->x][dum->y+1].visited){
                    cell_array[dum->x][dum->y+1].num=level+1;
                    cellStack.push(&cell_array[dum->x][dum->y+1]);
                }
            }
        }
        if(dum->down == false){
            if(dum->x+1<rows-1){
                if(!cell_array[dum->x+1][dum->y].visited){
                    cell_array[dum->x+1][dum->y].num=level+1;
                    cellStack.push(&cell_array[dum->x+1][dum->y]);
                }
            }
        }
    }
}

void Maze::getMaze(){
    for(int i=0;i<rows-1;i++){
        for(int j=0;j<cols-1;j++){
            cout<<cell_array[i][j].num<<" ";
        }
        cout<<'\n';
    }
}

void Maze::getShortestPath(){
    stack<int> coordinates;
    int x=rows-2;
    int y=cols-2;
    while(x!=0 || y!=0){
        coordinates.push(y);
        coordinates.push(x);
        int req_num = cell_array[x][y].num;
        if(cell_array[x][y].left == false && y-1>=0 && cell_array[x][y-1].num==req_num-1){
            y--;
        }
        else if(cell_array[x][y].up == false && x-1>=0 && cell_array[x-1][y].num==req_num-1){
            x--;
        }
        else if(cell_array[x][y].right == false && y+1<cols-1 && cell_array[x][y+1].num==req_num-1){
            y++;
        }
        else if(cell_array[x][y].down == false && x+1<rows-1 && cell_array[x+1][y].num==req_num-1){
            x++;
        }
        else{
            cout<<"No possible path exits...Random generation of coordinated will occur\n";
            break;
        } 
    }
    coordinates.push(0);
    coordinates.push(0);
    while(!coordinates.empty()){
        cout<<'('<<coordinates.top();
        coordinates.pop();
        cout<<','<<coordinates.top()<<')';
        coordinates.pop();
    }
}
int main(){
    int N,M;
    cin>>N>>M;
    Maze* maze=new Maze(N,M);
    maze->getShortestPath();
}