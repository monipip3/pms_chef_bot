[
  {
    $addFields:
      /**
       * newField: The new field name.
       * expression: The new field expression.
       */
      {
        new_id: {
          $toObjectId: "$_id",
        },
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
        from: "recipes_labels_phases",
        localField: "new_id",
        foreignField: "_id",
        as: "joined_docs",
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
        path: "$joined_docs",
      },
  },
  {
    $project:
      /**
       * specifications: The fields to
       *   include or exclude.
       */
      {
        new_id: 1,
        image_url: 1,
        title: "$joined_docs.title",
        ingredients:
          "$joined_docs.ingredientsArray",
        servings: "$joined_docs.servings_num",
        instructions:
          "$joined_docs.instructionsArray",
        dairy_free: "$joined_docs.dairy_free",
        gluten_free: "$joined_docs.gluten_free",
        pescatarian: "$joined_docs.pescatarian",
        vegetarian: "$joined_docs.vegetarian",
        nut_free: "$joined_docs.nut_free",
        cycle_phase: "$joined_docs.cycle_phase",
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
        from: "quality_control_recipes",
        localField: "_id",
        foreignField: "original_document_id",
        as: "qc_joined",
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
        path: "$qc_joined",
        preserveNullAndEmptyArrays: false,
      },
  },
  {
    $match:
      /**
       * query: The query in MQL.
       */
      {
        "qc_joined.remove_recipe": false,
      },
  },
  {
    $project:
      /**
       * specifications: The fields to
       *   include or exclude.
       */
      {
        new_id: 1,
        image_url: 1,
        title: 1,
        ingredients: 1,
        servings: 1,
        instructions: 1,
        dairy_free: 1,
        gluten_free: 1,
        pescatarian: 1,
        vegetarian: 1,
        nut_free: 1,
        cycle_phase: 1,
        free_version: "$qc_joined.top_recipe",
        breakfast: "$qc_joined.breakfast",
        lunch: "$qc_joined.lunch",
        dinner: "$qc_joined.dinner",
        snack: "$qc_joined.snack",
      },
  },
]