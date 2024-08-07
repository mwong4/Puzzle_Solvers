rm(list = ls())
cat("\014") 

# Init
mydata <- read.table("words.txt", sep=",", header=FALSE)
mydataprocessed <- data.frame(matrix(ncol = 5, nrow = 0))

# Add Data
for (d in mydata) {
  mydataprocessed <- rbind.data.frame(mydataprocessed, list(substring(d, 1, 1), substring(d, 2, 2), substring(d, 3, 3), substring(d, 4, 4), substring(d, 5, 5)))
}

# Fix col names
x <- c("char1", "char2", "char3", "char4", "char5")
colnames(mydataprocessed) <- x

for (i in colnames(mydataprocessed)){
  cat(i)
  cat(": ")
  copy <- mydataprocessed
  for (counter in 26:1) {
    most_common <- names(which.max(table(copy[,i])))
    cat(most_common)
    copy <- copy[copy[,i] != most_common,]
  }
  cat("\n")
}