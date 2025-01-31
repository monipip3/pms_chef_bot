[
  {
    $addFields:
      /**
       * newField: The new field name.
       * expression: The new field expression.
       */
      {
        new_id: {
          $toString: "$_id",
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
        from: "quality_control_recipes",
        localField: "new_id",
        foreignField: "original_document_id",
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
    $match:
      /**
       * query: The query in MQL.
       */
      {
        "joined_docs.remove_recipe": false,
      },
  },
  {
    $project:
      /**
       * specifications: The fields to
       *   include or exclude.
       */
      {
        title: 1,
        ingredients: 1,
        servings: 1,
        instructions: 1,
        query: 1,
      },
  },
]