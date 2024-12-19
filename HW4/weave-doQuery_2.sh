echo '{
  "query": "{
    Get{
      SimSearch (
        limit: 5
        nearText: {
          concepts: [\"Mercedes-Benz\", \"BMW M3\"]
        }
      ){
        brand
        model
        year
      }
    }
  }"
}' | curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -d @- \
  localhost:8080/v1/graphql
