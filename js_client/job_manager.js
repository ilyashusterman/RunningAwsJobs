
'use strict';

const e = React.createElement;

class JobManager extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        processing: false,
        response_content: {}
    };
  }
  initializeJob() {
    this.setState({ processing: true });
    let self = this;
    fetch('/api/process', {method:'POST'}).then(response => {
          let response_content = response.json();
          self.setState({'response_content': response_content})
        }
    );
    setInterval(this.setIntervalProcessCheck, 2000);
  }
  setIntervalProcessCheck() {
  if(this.processing) {
      clearInterval(timer);
      return;
    }
  else{
      
    }
  }
  render() {
    if (this.state.processing) {
      return 'Processing...';
    }

    return e(
      'button',
      { onClick: this.initializeJob },
      'Launch Job'
    );
  }
}

const domContainer = document.querySelector('#job_manager_container');
ReactDOM.render(e(JobManager), domContainer);