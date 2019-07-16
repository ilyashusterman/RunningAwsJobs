
'use strict';

const e = React.createElement;

class JobManager extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        processing: false,
        response_content: {},
        result_link: '',
        time: null
    };
  }
  initializeJob() {
    this.setState({ processing: true });
    let self = this;
    fetch('/api/process', {method:'POST'}).then(response => {
          let response_content = response.json();
          self.setState({
              'result_link': response_content,
              'processing': true
          })
        }
    );
    this.state.timer = setInterval(this.setIntervalProcessCheck.bind(this), 2000);
  }
  setIntervalProcessCheck() {
  let self = this;
  if(!self.state.processing) {
      clearInterval(this.state.timer);
      return;
    }
  else{
        fetch(self.state.result_link).then(response => {
          if (response.ok){
            self.setState({'processing': false,
            })
          }
        }
    );
    }
  }
  render() {
    if (this.state.processing) {
      return 'Processing...';
    }

    return e(
      'button',
      { onClick: this.initializeJob.bind(this) },
      'Launch Job link='+ this.state.result_link
    );
  }
}

const domContainer = document.querySelector('#job_manager_container');
ReactDOM.render(e(JobManager), domContainer);