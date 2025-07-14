import React from 'react';
import axios from 'axios';

export default class PersonList extends React.Component {
  state = {
    persons: []
  }

  componentDidMount() {
    axios.get(`http://127.0.0.1:8000/pinecone/medical`)
      .then(res => {
        console.log(res.data)
        const temp = res.data.replace(/&quot;/ig,'"');
        const persons = JSON.parse(JSON.stringify(temp));
        console.log(persons.result )
        this.setState({ persons });
      })
  }

  render() {
    return (
      <ul>
        {
          this.state.persons
            
        }
      </ul>
    )
  }
}