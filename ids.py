import copy
import time

class puzzle:

    def __init__(self,state,n,m,depth,pnum,pdir):#物件初始化
        self.state = state
        self.n = n
        self.m = m
        self.depth = depth
        self.pnum = pnum
        self.pdir = pdir

    def read_shape(self):#讀取方塊形狀
        global shape
        global maxnum
        num = 1
        found = True
        while(found==True):
            found = False
            rmin = -1
            rmax = -1
            cmin = -1
            cmax = -1
            for i in range(self.n):
                for j in range(self.m):
                    if int(self.state[i][j])==num:
                        found = True
                        if rmin==-1:
                            rmin = i
                        if i>rmax:
                            rmax = i
                        if cmin==-1:
                            cmin = j
                        if j>cmax:
                            cmax = j
            if found:         
                shape[num] = [rmax-rmin+1,cmax-cmin+1]
            num += 1
        maxnum = num-1

    def final_state(self):#生成final state
        global shape
        global final_state_row
        num = 1
        start = [[0 for _ in range(self.m)] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                if start[i][j] == 0 and num in shape:
                    for r in range(int(shape[num][0])):
                        for c in range(int(shape[num][1])):
                            start[i+r][j+c] = str(num)
                    final_state_row[str(num)] = [i,j]
                    num+=1
                
        return start
    
    def can_move(self,num,dir,step):#判斷編號為num的方塊能否向dir移動step步(dir:上(0)右(1)下(2)左(3)
        old = []
        row = [-1,0,1,0]
        col = [0,1,0,-1]
        tar_pos = []
        ori_pos = []
        exist = False
        for i in range(self.n):
            for j in range(self.m):
                if num==int(self.state[i][j]):
                    exist = True
                    trow = i+int(row[dir]*step)
                    tcol = j+int(col[dir]*step)
                    tar_pos.append([trow,tcol])
                    ori_pos.append([i,j])
                    if trow<self.n and tcol<self.m and trow>=0 and tcol>=0:
                        old.append(self.state[trow][tcol])
                    else:
                        return False

        for x in old:
            if int(x)!=int(num) and int(x)!=0:
                return False

        for pos in tar_pos:
            if int(pos[0]) > self.n-1 or int(pos[0]) < 0:
                return False
            if int(pos[1]) > self.m-1 or int(pos[1]) < 0:
                return False
        if exist:
            return True
        else:
            return False
        
    def move(self,num,dir,step):#將編號為num的方塊向dir移動step步(dir:上(0)右(1)下(2)左(3)dir:上(0)右(1)下(2)左(3)
        next_state = copy.deepcopy(self.state)
        row = [-1,0,1,0]
        col = [0,1,0,-1]
        tar_pos = []
        ori_pos = []
        for i in range(n):
            for j in range(m):
                if num==int(self.state[i][j]):
                    trow = i+int(row[dir]*step)
                    tcol = j+int(col[dir]*step)
                    tar_pos.append([trow,tcol])
                    ori_pos.append([i,j])

        for pos in ori_pos:
            next_state[int(pos[0])][int(pos[1])] = '0'

        for pos in tar_pos:
            next_state[int(pos[0])][int(pos[1])] = str(num)

        return next_state
        
    def is_final_state(self):#判斷是否為final state
        max = 0
        past = []
        for i in range(self.n):
            for j in range(self.m):
                if int(self.state[i][j]) > max:
                    max = int(self.state[i][j])
                    past.append(int(self.state[i][j]))
                    continue
                elif int(self.state[i][j])==0:
                    continue
                elif int(self.state[i][j]) in past:
                    continue
                else:
                    return False
        return True

    def iddfs(self,dlimit):#進行IDDFS search
        global final
        global ans
        if(final):
            return
        for i in range(1,maxnum+1):
            for j in range(4):
                if self.can_move(i,j,1):
                    if i != self.pnum or abs(j-self.pdir)!=2:
                        next_state = self.move(i,j,1)
                        next = puzzle(next_state,self.n,self.m,self.depth+1,i,j)
                        if(self.is_final_state()):
                            final = True
                            return True
                        elif self.depth<=dlimit:
                            if next.iddfs(dlimit):
                                ans.append([i,j])
        return final


start = time.time()
#變數宣告
input = []
ans = []
IDAans = []
final = False
final2 = False
shape = {}
final_state_row = {}
maxnum = 0
#輸入處理
with open('5*4.txt') as f:
    lines = f.readlines()
f_out = open('output.txt','w')
n,m = lines[0].split()
n = int(n)
m = int(m)
for i in range(1,n+1):
    x = lines[i].split()  
    input.append(x)
now_puzzle = puzzle(input,n,m,1,0,0)
now_puzzle.read_shape()
puzzle_final_state = now_puzzle.final_state()
#IDDFS
for i in range(1,30):
    if not final:
        now_puzzle.iddfs(i)
#輸出處理
ans.reverse()
move = ['U','R','D','L']
end = time.time()
f_out.write('Total run time = '+str(round(end-start,3))+'seconds.\n')
f_out.write('An optional solution has '+str(len(ans))+' moves :\n')
for step in ans:
    print(str(step[0])+move[step[1]],file = f_out,end=' ')
f_out.close()
