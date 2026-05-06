WITH
  cleaned_data AS (
    SELECT
      year,
      CASE
        WHEN LOWER(TRIM(make)) IN ('dodge', 'tk', 'dot')
          THEN
            'Dodge'  -- Mapping 'Dodhe' as requested but assuming typo for 'Dodge'
        WHEN LOWER(TRIM(make)) LIKE 'ford%' THEN 'Ford'
        WHEN LOWER(TRIM(make)) = 'vw' THEN 'Volkswagen'
        WHEN LOWER(TRIM(make)) LIKE 'mazda%' THEN 'Mazda'
        WHEN LOWER(TRIM(make)) LIKE 'mercedes%' THEN 'Mercedes-Benz'
        WHEN
          LOWER(TRIM(make)) LIKE 'land rober%'
          OR LOWER(TRIM(make)) LIKE 'land rover%'
          THEN 'Land Rover'
        WHEN LOWER(TRIM(make)) LIKE 'hyundai%' THEN 'Hyundai'
        WHEN LOWER(TRIM(make)) LIKE 'gmc%' THEN 'GMC'
        ELSE INITCAP(NULLIF(TRIM(make), ''))
        END
        AS maker,
      INITCAP(NULLIF(TRIM(model), '')) AS model,
      INITCAP(NULLIF(TRIM(body), '')) AS body,
      INITCAP(NULLIF(TRIM(transmission), '')) AS transmission,
      UPPER(NULLIF(TRIM(state), '')) AS state,
      condition,
      odometer,
      INITCAP(NULLIF(TRIM(color), '')) AS color,
      INITCAP(NULLIF(TRIM(interior), '')) AS interior,
      INITCAP(NULLIF(TRIM(seller), '')) AS seller,
      mmr,
      sellingprice,
      NULLIF(TRIM(saledate), '') AS saledate,
      ratio_after,
      flag_outlier
    FROM `lunar-carving-457020-h5.YuseiSQL.cleaned_car_prices`
        WHERE flag_outlier IS NOT TRUE
  )
SELECT * FROM cleaned_data;

