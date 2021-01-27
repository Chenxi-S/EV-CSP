library(raster)
library(sp)
library(rgdal)
library(rgeos)

# set working directory to data folder
#getwd()
setwd('d:/data/')

# load data
DEM <- raster("landscan2018/lspop2018/sta.adf")

# plot the raster
# note that this raster represents a small region of the NEON SJER field site
plot(DEM, 
     main="Landscan 2018") # add title with main
# or use image function,no legend 
# image(DEM) 

# crop raster in R with polygon 
#(ISSUE: cropped, but not fully cropped)
p <- shapefile("sz_shape/shenzhen-polygon.shp")
pb <- crop(p, DEM)

# mask working!
p <- shapefile("sz_shape/shenzhen-polygon.shp")
sz <- mask(DEM,p)
# specify the range of lat and lon for compact plot
# sz : nrol 76, ncol 146
# crop the redundant area (not much difference)
sz_compact <- crop(sz, extent(sz, 20, 70, 20, 140))
plot(sz_compact)

# convert to dataframe 
# IMPORTANT!:Replace COUNT with ID (count is not pop, but ID is)
# reference: https://stackoverflow.com/questions/50463141/
# convert-a-raster-to-a-dataframe-and-extract-values-you-want-in-r
RAT<- levels(sz)[[1]]
RAT$pop <- RAT$ID
RAT$COUNT <- NULL
sz1 <- sz
levels(sz1)[[1]] <- RAT
# Create a single layer based on the new RAT
sz1 <- deratify(sz1)
# Create a data frame
sz_pop <-as.data.frame(sz1, xy = TRUE)

# remove NA(empty grids),2520 in total 
sz_pop <- sz_pop[complete.cases(sz_pop), ]
nrow(sz_pop)

# save as csv file
write.csv(sz_pop,"sz_pop.csv")


# xyz to raster
sz_pop <- read.csv("C:/Users/sunchenxi/Dropbox/data/sz_pop.csv")
r <- rasterFromXYZ(sz_pop[, c('x', 'y', 'pop')])
plot(r)

# plot selected grids on top of that
#selected_id <- c(2161, 2207, 2160, 2208, 2162, 2104, 2163, 2209, 2105, 2210, 2106, 2232, 2164, 2206, 2159, 2275, 2107, 2186, 2211, 2316, 2252, 2291, 2187, 2103, 2253, 2033, 2254, 2256, 2165, 2255, 2233, 2032, 2212, 2250, 2276, 2289, 2251, 2292, 2031, 2418)
selected_id <- c(2161, 2232, 2164, 2291, 2206, 2418, 1942, 2275, 2104, 2210, 2289, 209, 2250, 497, 2186, 1970, 126, 2109, 2207, 653, 570, 2316, 99, 1470, 1662, 2189, 1945, 266, 2107, 253, 630, 2244, 1941, 2159, 658, 2208, 2417, 473, 60, 2326)
selected_id <- selected_id+1
selected <- sz_pop[selected_id[1:20], ]
r_selected<- rasterFromXYZ(selected[, c('x', 'y', 'pop')])
plot(r,legend=FALSE)
plot(r_selected,col='black',legend=FALSE,add=TRUE)
