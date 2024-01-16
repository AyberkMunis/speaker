import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import { CssBaseline, InputLabel, MenuItem, Select, ThemeProvider } from "@material-ui/core";
import { createTheme } from '@material-ui/core/styles';
import CreateRoomPage from "./CreateRoomPage";
import MusicPlayer from "./musicplayer";

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


export default class Room extends Component {
  constructor(props) {
    super(props);
    this.state = {
      genre: "Annen",
      taste: "Baban",
      base: "Deden",
      name:"",
      isHost:"",
      showsettings:false,
      successMsg:"",
      errorMsg:"",
      song:{},
      message:"",
      send:false,
      msg2:"",
    };
    this.roomCode = this.props.match.params.roomCode;
    this.getRoomDetails=this.getRoomDetails.bind(this)
    this.leaveButtonPressed=this.leaveButtonPressed.bind(this)
    this.updateshowsettings=this.updateshowsettings.bind(this)
    this.rendersettingsbutton=this.rendersettingsbutton.bind(this)
    this.renersettings=this.renersettings.bind(this)
    this.handleUpdateButton=this.handleUpdateButton.bind(this)
    this.authenticateSpotify=this.authenticateSpotify.bind(this)
    this.getCurrentSong=this.getCurrentSong.bind(this)
    this.getRoomDetails()

    }
  componentDidMount(){
    this.interval =setInterval(this.getCurrentSong,1000)
  }
  componentWillUnmount(){
    clearInterval(this.interval);
  }

  getRoomDetails() {
    fetch("/spotify/getu-taste");
    return fetch("/api/get-room" + "?code=" + this.roomCode)
      .then((response) => {
        if (!response.ok) {
          this.props.leaveRoomCallback();
          this.props.history.push("/");
        }
        return response.json();
      })
      .then((data) => {
        this.setState({
          genre: data.genre,
          taste: data.taste,
          base:data.base,
          isHost: data.is_host,
          name:data.name,

        });
      });
  }
  leaveButtonPressed() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };
    fetch("/api/leave-room", requestOptions).then((_response) => {
      this.props.leaveRoomCallback();
      this.props.history.push("/");
    });
  }
  authenticateSpotify() {
    fetch("/spotify/is-authenticated")
      .then((response) => response.json())
      .then((data) => {
        this.setState({ spotifyAuthenticated: data.status });
        console.log(data.status);
        if (!data.status) {
          fetch("/spotify/get-auth-url")
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url);
            });
        }
      });
  }
  getCurrentSong(){
    fetch("/spotify/get-current").then((response)=>
    {
      if(!response.ok){
        return {}
      }
      else{
        return response.json()
      }

    }).then((data)=>this.setState({ song: data }))
  }
  updateshowsettings(value){
    this.setState({
      showsettings:value
    })

  }
  rendersettingsbutton(){
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline/>
        <Grid container spacing={3}>
          <Grid item xs={12} align="center">
            <Button variant="contained" color="primary" onClick={()=>this.updateshowsettings(true)}>
              Settings
            </Button>

          </Grid>
        </Grid>
      </ThemeProvider>
    );
  }
  handleBase(e){
    this.setState({
        base:e.target.value,
        
    });
}
  rendertext(){
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline/>
        <Grid container spacing={3}>
        <Grid item xs={12} align="center">
                <FormControl>
                    <TextField required={false} label="Message" onChange={this.handlemsg} sx={{"& label": {color: "primary.main"}}}></TextField>
                </FormControl>
                <Button
            color="primary"
            variant="contained"
            onClick={this.handlbtn}
        >
            Send
                </Button>
            </Grid>
        </Grid>
      </ThemeProvider>
    );
  }
  handleUpdateButton(){
      const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            genre:this.state.genre,
            code:this.props.roomCode
          }),
        };
        fetch("/api/update-room", requestOptions)
          .then((response) => {
            if(response.ok){
              this.setState({
                successMsg:"Room Updated Succesfully"
              })

            }else{
              this.setState({
                errorMsg:"Error Updating Room"
              })

            }
          })
      }
  renersettings(){
    return (
      <ThemeProvider theme={theme}>
      <CssBaseline/>
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <CreateRoomPage
            update={true}
            genre={this.state.genre}
            roomCode={this.roomCode}
            updateCallback={this.getRoomDetails}
          />
        </Grid>
        <Grid item xs={12} align="center">
          <Button
            variant="contained"
            color="secondary"
            onClick={() => this.updateshowsettings(false)}
          >
            Close
          </Button>
        </Grid>
      </Grid>
      </ThemeProvider>
    )
  }


  render() {
    if( this.state.showsettings){
      return this.renersettings();  
    }
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline/>
        <Grid container spacing={2}>
            <Image src={"https://i.ibb.co/mBWPZws/room2.png"} />


          <Grid item xs={12} align="center">
            <Typography variant="h3" component="h3" >
              {this.state.name} Code:{this.roomCode} 
            </Typography>

          </Grid>
            <MusicPlayer {...this.state.song} />
          <Grid item xs={12} align="center">
          {this.state.isHost ? this.rendersettingsbutton() : null}
          </Grid>
          <Grid item xs={12} align="center">
            <Button variant="contained" color="primary" onClick={this.leaveButtonPressed}>
                Leave the Place
              </Button>
             </Grid>
        </Grid>
      </ThemeProvider>
    );
  }
}