library(readr)
library(data.table)

if (Sys.getenv("USERNAME") == "manma"){
  data_path <- "D:/Dropbox/small-biz-2020/data"
}

d <- read_csv(paste(data_path, 'us', 'us_countries.csv', sep='/'))
p <- read_csv(paste(data_path, 'us', 'us_county_pop.csv', sep='/'))

p = data.table(p)
n <- p[,  strsplit(county, split = ", ")]

for (j in 1:(length(n))) {
  p[j, county := n[[j]][1]]
  p[j, state:= n[[j]][2] ]
}
p[, county := gsub( " County", "", county)]


d <- data.table(d)

dd <- d[, .("deaths" = sum(deaths, na.rm = T),
            "cases" = sum(cases, na.rm = T)), by = .(state,county) ]

D <- merge(dd,p, by = c("state","county"), all = F)

D[ , death_scaled := round(deaths / pop, 6)]
D[order(death_scaled)]

D[ , cases_scaled := round(cases / pop, 6)]
D[order(death_scaled)]

D[, ind :=  cases_scaled/sd(cases_scaled) + death_scaled/sd(death_scaled)]
