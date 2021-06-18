# See https://ciakovx.github.io/rorcid.html for a full walkthrough, including explanatory text

# See https://mybinder.org/v2/gh/ciakovx/ciakovx.github.io/master?filepath=rorcid.ipynb for a 
# Binder link to a Jupyter Notebook to try this out in your browser 



# Install and load packages -----------------------------------------------

# you will need to install these packages first, using the following
# if you've already installed them, skip this step
install.packages('rorcid')
install.packages('tidyverse')
install.packages('usethis')
install.packages('anytime')
install.packages('janitor')
install.packages('glue')

# load the packages
library(rorcid)
library(usethis)
library(tidyverse)
library(anytime)
library(lubridate)
library(janitor)
library(glue)

# authorize ORCID API (should prompt a window to open in your browser to login to your ORCID account)
orcid_auth(reauth=TRUE)


# build the query  --------------------------------------------------------

ringgold_id <- "6429" 
grid_id <- "grid.168010.e" 
email_domain <- "@stanford.edu" 
organization_name <- "Stanford University"

# example
# ringgold_id <- "7618"
# grid_id <- "grid.65519.3e"
# email_domain <- "@okstate.edu"
# organization_name <- "Oklahoma State University"

# create the query
my_query <- glue('ringgold-org-id:',
                 ringgold_id,
                 ' OR grid-org-id:',
                 grid_id,
                 ' OR email:*',
                 email_domain,
                 ' OR affiliation-org-name:"',
                 organization_name,
                 '"')

# get the counts
orcid_count <- base::attr(rorcid::orcid(query = my_query), "found")

# create the page vector
my_pages <- seq(from = 0, to = orcid_count, by = 200)

# get the ORCID iDs
my_orcids <- purrr::map(
  my_pages,
  function(page) {
    print(page)
    my_orcids <- rorcid::orcid(query = my_query,
                               rows = 200,
                               start = page)
    return(my_orcids)
  })

# put the ORCID iDs into a single tibble
my_orcids_data <- my_orcids %>%
  map_dfr(., as_tibble) %>%
  janitor::clean_names()



# get employment data -----------------------------------------------------

# get the employments from the orcid_identifier_path column
# be patient, this may take a while
my_employment <- rorcid::orcid_employments(my_orcids_data$orcid_identifier_path)

# extract the employment data from the JSON file and mutate the dates
my_employment_data <- my_employment %>%
  purrr::map(., purrr::pluck, "affiliation-group", "summaries") %>% 
  purrr::flatten_dfr() %>%
  janitor::clean_names() %>%
  dplyr::mutate(employment_summary_end_date = anytime::anydate(employment_summary_end_date/1000),
                employment_summary_created_date_value = anytime::anydate(employment_summary_created_date_value/1000),
                employment_summary_last_modified_date_value = anytime::anydate(employment_summary_last_modified_date_value/1000))

# clean up the column names
names(my_employment_data) <- names(my_employment_data) %>%
  stringr::str_replace(., "employment_summary_", "") %>%
  stringr::str_replace(., "source_source_", "") %>%
  stringr::str_replace(., "organization_disambiguated_", "")

# view the unique institutions in the organization names columns
# keep in mind this will include all institutions a person has in their employments section
my_organizations <- my_employment_data %>%
  group_by(organization_name) %>%
  count() %>%
  arrange(desc(n))

# you can also filter it with a keyword:
my_organizations_filtered <- my_organizations %>%
  filter(str_detect(organization_name, "Oklahoma"))

# filter the dataset to include only the institutions you want. 
# As you can see in the below example, there may be messiness in the hand-entered ones
# See example:
my_employment_data_filtered <- my_employment_data %>%
  dplyr::filter(organization_name == "Oklahoma State University Stillwater"
                | organization_name == "Oklahoma State University Tulsa"
                | organization_name == "Oklahoma State University"
                | organization_name == "Oklahoma State University "
                | organization_name == "Oklahoma State University System"
                | organization_name == "Oklahoma State University Oklahoma Agricultural Experiment Station"
                | organization_name == "Oklahoma State University Center for Veterinary Sciences"
                | organization_name == "Oklahoma State University, Stillwater"
                | organization_name == "College of Veterinary Medicine, Oklahoma State University"
                | organization_name == "Interim Dean, College of Education, Health & Aviation, Oklahoma State University"
                | organization_name == "Oklahoma state university")

# finally, filter to include only people who have NA as the end date
my_employment_data_filtered_current <- my_employment_data_filtered %>%
  dplyr::filter(is.na(end_date_year_value),
                !is.na(orcid_uri))


# Education ---------------------------------------------------------------

# you can also get data on people whose degree information includes your university
# then filter that to get current students
my_education <- rorcid::orcid_educations(my_orcids_data$orcid_identifier_path)

# then generally follow the steps above, making modifications to variable names as necessary.
my_education_data <- my_education %>%
  purrr::map(., purrr::pluck, "affiliation-group", "summaries") %>% 
  purrr::flatten_dfr() %>%
  janitor::clean_names() %>%
  dplyr::mutate(education_summary_end_date = anytime::anydate(education_summary_end_date/1000),
                education_summary_created_date_value = anytime::anydate(education_summary_created_date_value/1000),
                education_summary_last_modified_date_value = anytime::anydate(education_summary_last_modified_date_value/1000))
names(my_education_data) <- names(my_education_data) %>%
  stringr::str_replace(., "education_summary_", "") %>%
  stringr::str_replace(., "source_source_", "") %>%
  stringr::str_replace(., "organization_disambiguated_", "")
my_education_organizations <- my_education_data %>%
  group_by(organization_name) %>%
  count() %>%
  arrange(desc(n))
my_education_data_filtered <- my_education_data %>%
  dplyr::filter(organization_name == "Oklahoma State University Stillwater"
                | organization_name == "Oklahoma State University Tulsa"
                | organization_name == "Oklahoma State University"
                | organization_name == "Oklahoma State University "
                | organization_name == "Oklahoma State University System")
my_education_data_filtered_current <- my_education_data_filtered %>%
  dplyr::filter(is.na(end_date_year_value),
                !is.na(orcid_uri))

