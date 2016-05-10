library(jsonlite)
library(arules)
library(XML)

setwd("C:\\Users\\Nolan\\Documents\\My Programs\\Search Results")

# Import the organizations and people Crunchbase csv files
organizations <- read.csv("~/School/CSC595-Big Data/Project5-PatentsAndCompanies/organizations.csv")
people <- read.csv("~/School/CSC595-Big Data/Project5-PatentsAndCompanies/people.csv")
people$organization <- tolower(people$organization)



# Combine the first and last names of people in organizations and people
ppl <- cbind(people, tolower(paste(people$first_name, people$last_name, sep = " ")))
colnames(ppl)[length(ppl)] <- c("full_name")


# Run the python program
setwd("C:\\Users\\Nolan\\Documents\\My Programs\\Search Results")

# Import all the search result files
files <- read.csv("result_files.txt", header = FALSE)

# GetFiles function: Con
#   The patent_analysis.py program will create a file containing all the 
GetFiles <- function(fFrame){
  # Use levels() to obtain a list of all file names in fFrame
  lvls <- levels(fFrame[,1])
  
  # Empty list that will store each JSON results file
  aggResults <- list()
  
  # Get each JSON file and flatten it into a table structure
  for (i in 1:length(lvls)){
    tmpFile <- fromJSON(lvls[i], flatten = TRUE)
    
    # Add the JSON file data to the tmp file
    aggResults[[i]] <- tmpFile
  }
  
  # Return the aggregate results as a list of data.frames
  aggResults
}

ExtractPatentInfo <- function(aggRes){
  df <- data.frame(matrix(nrow = 1, ncol = 6))
  
  # Loop through all members of aggRes
  for (i in 2:length(aggRes)){
    for (j in 1:length(aggRes[i][[1]]$items$pagemap.metatags)){

      contributor <- tolower(aggRes[i][[1]]$items$pagemap.metatags[[j]]$dc.contributor)
      title <- aggRes[i][[1]]$items$pagemap.metatags[[j]]$dc.title
      file_date <- aggRes[i][[1]]$items$pagemap.metatags[[j]]$dc.date
      id <- aggRes[i][[1]]$items$pagemap.metatags[[j]]$dc.relation
      tot_results <- aggRes[i][[1]]$queries$request$totalResults
      search_terms <- aggRes[i][[1]]$queries$request$searchTerms
      
      x <- c(contributor, title, id, file_date, tot_results, search_terms)
      
      # Add the element to the data.frame
      df <- rbind(df, data.frame(matrix(x, nrow = 1, ncol = 6)))
    }
  }
  colnames(df) <- c("Contributor", "Title", "Patent.id","File.date", "Total.results","Search.terms")
  
  # Return...
  df
}

# Consolodate the seach results
test <- GetFiles(files)

# Extract the patent title, contributor name, and date
pFrame <- ExtractPatentInfo(test)
print(pFrame)
write.csv(pFrame, file = "PatentTitlesContributors.csv")


