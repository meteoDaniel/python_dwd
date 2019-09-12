""" time resolution to parameter mapping """

TIME_RESOLUTION_PARAMETER_MAPPING = {
    "1_minute": [["precipitation"],
                 ["historical",
                  "recent",
                  "now"]],
    "10_minutes": [["air_temperature",
                    "extreme_temperature",
                    "extreme_wind",
                    "precipitation",
                    "solar",
                    "wind"],
                   ["historical",
                    "recent",
                    "now"]],
    "hourly": [["air_temperature",
                "cloud_type",
                "cloudiness",
                "precipitation",
                "pressure",
                "soil_temperature",
                "solar",
                "sun",
                "visibility",
                "wind"],
               ["historical",
                "recent"]],
    "daily": [["kl",
               "more_precip",
               "soil_temperature",
               "solar",
               "water_equiv"],
              ["historical",
               "recent"]],
    "monthly": [["kl",
                 "more_precip"],
                ["historical",
                 "recent"]],
    "annual": [["kl",
                "more_precip"],
               ["historical",
                "recent"]]
}