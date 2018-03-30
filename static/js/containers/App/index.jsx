import React, { Component } from 'react'
import { gql } from 'apollo-boost'
import { Query } from 'react-apollo'
import './style.css'

const GET_TEACHERS = gql`
  query {
    allTeachers {
      edges {
        node {
          name
          hiredOn
          department {
            name
          }
        }
      }
    }
  }
`

export default class App extends Component {
  render() {
    return (
      <Query query={GET_TEACHERS}>
        {({ loading, error, data }) => {
          if (loading) return <div>Loading...</div>
          if (error) return <div>THERE WAS AN ERROR</div>
          console.log(data)
          return <div>{data.allTeachers.edges[0].node.name}</div>
        }}
      </Query>
    )
  }
}
