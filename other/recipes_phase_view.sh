[
  {
    $lookup:
      /**
       * path: Path to the array field.
       * includeArrayIndex: Optional name for index.
       * preserveNullAndEmptyArrays: Optional
       *   toggle to unwind null and empty values.
       */
      {
        from: "ingredients",
        localField: "query",
        foreignField: "Ingredient",
        as: "joined",
      },
  },
  {
    $unwind:
      /**
       * path: Path to the array field.
       * includeArrayIndex: Optional name for index.
       * preserveNullAndEmptyArrays: Optional
       *   toggle to unwind null and empty values.
       */
      {
        path: "$joined",
        includeArrayIndex: "string",
        preserveNullAndEmptyArrays: true,
      },
  },
  {
    $lookup:
      /**
       * from: The target collection.
       * localField: The local join field.
       * foreignField: The target join field.
       * as: The name for the results.
       * pipeline: Optional pipeline to run on the foreign collection.
       * let: Optional variables to use in the pipeline field stages.
       */
      {
        from: "recipe_image_data",
        localField: "_id",
        foreignField: "_id",
        as: "joined2",
      },
  },
  {
    $unwind:
      /**
       * path: Path to the array field.
       * includeArrayIndex: Optional name for index.
       * preserveNullAndEmptyArrays: Optional
       *   toggle to unwind null and empty values.
       */
      {
        path: "$joined2",
        includeArrayIndex: "string",
        preserveNullAndEmptyArrays: true,
      },
  },
  {
    $project:
      /**
       * specifications: The fields to
       *   include or exclude.
       */
      {
        _id: 1,
        title: 1,
        servings_num: 1,
        instructionsArray: 1,
        ingredientsArray: 1,
        query: 1,
        vegetarian: 1,
        pescatarian: 1,
        gluten_free: 1,
        dairy_free: 1,
        nut_free: 1,
        cycle_phase: "$joined.cycle_phase",
        image_url: "$joined2.image_url",
      },
  },
]