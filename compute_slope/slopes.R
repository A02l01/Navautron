library(ggplot2)
library(tidyr)
library(dplyr)
library(segmented)
library(cowplot)
library(progress)

compute_slope<-function(d,N,myfile){
  #N=1
  rout=NULL
  deja = NULL
  if(file.exists(myfile)){
    deja = read.csv(myfile,sep='\t',header=F)
  }
  
  for(uy in levels(as.factor(d$UId))){
    mpass=F
    if(length(deja$V1)!=0){#length(deja$V1)!=0length(deja)==0
      if((uy %in% deja$V1)==T){
        mpass = T
      }
    }
    if(mpass == F){
      sd = subset(d,subset=c(UId==uy))
      min = 0 
      mm = max(sd$S)*0.5
      mm = (max(sd$S)-min(sd$S))*0.5
      ts = sd$t[which.max(abs(sd$S))]
      ssd = subset(sd,subset=c(t<ts))
      max = ssd$t[which.min(abs(ssd$S-mm))]
      span=30
      mfit = with(sd,ksmooth(t,S,kernel = "normal",bandwidth = span))
      
      p = ggplot()+geom_point(data=sd,aes(x=t,y=S),alpha=0.3)+
        geom_line(aes(x=sd$t,y=mfit$y),color='black')+
        theme_bw()+ggtitle(uy)+
        geom_vline(xintercept = max,color='red')
      print(p)
      sd$Sb = as.numeric(mfit$y)
      minmax = readline(paste0("Enter limit  [range,[s]=skip,[a]=automatic]> "))
      if(minmax!="s"){
        if(minmax != "a"){
          min = as.numeric(unlist(strsplit(minmax,","))[[1]])
          max = as.numeric(unlist(strsplit(minmax,","))[[2]])
        }
        sd = subset(sd,subset=c(UId==uy & t>min & t < max))
        print(N)
        N = N+1
        x = sd$t
        y = log(sd$Sb+1E-9)
        y[which(y==-Inf)] = NA
        
        # plot(y~x)
        
        if(is.na(sum(y))!=TRUE){
          for(jj in 1:1){
            out.lm = lm(y~x)
            o <- segmented(out.lm, seg.Z = ~ x)
            fit <- numeric(length(x)) * NA
            fit[complete.cases(rowSums(cbind(y, x)))] <- broken.line(o)$fit
            if(jj == 1){
              val = sd(o$residuals)
              y[which(o$residuals > val | o$residuals < -val)]=NA
            }
          }
          o$coefficients
          
          
          data1 <- data.frame(x =x, y = y, fit = fit)
          res = slope(o)
          
          p1 = ggplot()+geom_point(data=filter(sd,S>1),aes(x=t,y=log(S+1E-9)),alpha=0.3)+
            geom_line(data=data1,aes(x=x,y=y),color="black")+
            geom_line(aes(x=x,y=fit),color="steelblue")+theme_bw()+
            geom_vline(xintercept = o$psi[[2]],color="red")+
            # geom_text(aes(x=o$psi[[2]]+0.5*(max-o$psi[[2]]),y=min(y)+(max(y)-min(y))*0.5,label=res$x[2,1]))+
            ggtitle(paste(uy,res$x[2,1],sep=" "))
          p2 = ggplot()+
            geom_line(data = data1,aes(x=x,y=exp(y)),alpha=0.3)+
            geom_point(data=sd,aes(x=t,y=S),alpha=0.3)+
            theme_bw()+geom_vline(xintercept = o$psi[[2]],color="red")
          
          p = plot_grid(p1,p2,ncol=2,nrow=1, align="hv")
          print(p)
          answer<-readline(paste("Is it ok: \n \t please >> enter O,N : \n Enter Your Response HERE:   ",sep=""))
          rout = rbind(rout,c(uy,o$psi[[2]],res$x[2,1],sd$mod[1],answer))
          print(sd$mod[1])
          # line = paste(uy,o$psi[[2]],res$x[2,1],sd$mod[1],answer,sep="\t")
          line = paste(uy,o$psi[[2]],res$x[2,1],answer,sep="\t")
          write(line,file=myfile,append=TRUE)
        }
      }
      if(minmax=="s"){
        # line = paste(uy,NA,NA,NA,minmax,sep="\t")
        line = paste(uy,NA,NA,minmax,sep="\t")
        write(line,file=myfile,append=TRUE)
      }
    }## fin uy
  }
  
  return(rout)
}

