echo '{
  "query": "{
    Get{
      SimSearch (
        limit: 3
        nearText: {
          concepts: [\"physics\"],
        }
      ){
        question
        answer
        category
      }
    }
  }"
}'  | curl \
    -X POST \
    -H 'Content-Type: application/json' \
    -d @- \
    localhost:8080/v1/graphql