cat("\014") 

most_repeated_character <- function(x) {
  tab <- table(strsplit(x, '')[[1]])
  names(tab)[tab == max(tab)]
}

file <- '../words.txt'
mydata <- readChar(file, file.info(file)$size)
# Prune whitespace
mydata <- invisible(gsub(" ", "", mydata))
mydata <- invisible(gsub("\n", "", mydata))
mydata <- invisible(gsub("\r", "", mydata))

for (counter in 26:1) {
  most_common <- most_repeated_character(mydata)
  #print(paste("[", most_common, ": ", counter, "]"))
  cat(most_common)
  mydata <- invisible(gsub(most_common, "", mydata))
}
