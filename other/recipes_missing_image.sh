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
       * path: Path to the array field.
       * includeArrayIndex: Optional name for index.
       * preserveNullAndEmptyArrays: Optional
       *   toggle to unwind null and empty values.
       */
      {
        from: "recipe_images",
        localField: "new_id",
        foreignField: "_id",
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
        includeArrayIndex: "joined",
        preserveNullAndEmptyArrays: true,
      },
  },
  {
    $match:
      /**
       * query: The query in MQL.
       */
      {
        joined: null,
        /**joined: {
    $ne: null, */
      },
  },
]