import React, { Component } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";
import { Button, ButtonGroup, Grid, ThemeProvider, Typography } from "@material-ui/core";
import { createTheme } from '@material-ui/core/styles';
import { Image } from 'mui-image'
const theme = createTheme({
  palette: {
    primary: {
      main:"#191414",
    },
    secondary: {
      main: "#ffffff",
    },
    text:{
      primary:"#191414"

    }
  },
});

export default class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state={
      roomCode:null,
      spotifyAuthenticated:false,
    }
    this.clearRoomCode=this.clearRoomCode.bind(this)
    this.authenticateSpotify=this.authenticateSpotify.bind(this)
    this.authenticateSpotify()

  }

  async componentDidMount(){
      fetch('/api/user-in-room').then((response)=>response.json())
      .then((data)=>{this.setState({
        roomCode:data.code
      })})
  }
  renderHomePage(){
    return(
      <ThemeProvider theme={theme}>
        <Grid container spacing={3}>
        <Image
                src="https://i.ibb.co/6ZtY2DZ/Homepage2.png"
          />
        <Grid item xs={12} align="center">
          <ButtonGroup disableElevation variant="contained" color="primary">
            <Button color="primary" to="/join" component={Link} >
              Join Place
            </Button>
            <Button color="primary" to="/create" component={Link} >
              Create Place
            </Button>
          </ButtonGroup>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography variant="h5" component={"h5"}>
            Created by Ayberk Munis & Alp Tutar
          </Typography>
        </Grid>

        </Grid>
      </ThemeProvider>

    )
  }
  clearRoomCode(){
    this.setState({
      roomCode:null
    })
  }
  authenticateSpotify(){
    fetch('spotify/is-authenticated').then((response)=>response.json()).then((data)=>{
      this.setState({spotifyAuthenticated:data.status});
      if(!data.status){
        fetch("/spotify/get-auth-url").then((response)=>response.json()).then((data)=>{
          window.location.replace(data.url);
        })
      }
    })
  }

  render() {
    return (
      <Router>
        <Switch>
        <Route
            exact
            path="/"
            render={() => {
              return this.state.roomCode ? (
                <Redirect to={`/room/${this.state.roomCode}`} />
              ) : (
                this.renderHomePage()
              );
            }}
          />  
          <Route path="/join" component={RoomJoinPage} />
          <Route path="/create" component={CreateRoomPage} />
          <Route
            path="/room/:roomCode"
            render={(props) => {
              return <Room {...props} leaveRoomCallback={this.clearRoomCode} />;
            }}
          />
        </Switch>
      </Router>
    );
  }
}
