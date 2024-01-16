import React,{Component} from "react";
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
import { CssBaseline, InputLabel, MenuItem, Select } from "@material-ui/core";
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
import { Image } from 'mui-image'
import Alert from "@material-ui/lab/Alert"
import Collapse from "@material-ui/core/Collapse";
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
export default class CreateRoomPage extends Component{
    static defaultProps = {
        votesToSkip: 2,
        guestCanPause: true,
        update: false,
        roomCode: null,
        updateCallback: () => {},
      };
    constructor(props){
        super(props);
        this.state={
            name:"",
            taste:{},
            base:"",
            genre:"pop rap",
            errorMsg: "",
            successMsg: "",
        }
        this.handleName=this.handleName.bind(this)
        this.handleBase=this.handleBase.bind(this)
        this.createR=this.createR.bind(this)
        this.handleGnere=this.handleGnere.bind(this)
        this.handleUpdateButtonPressed=this.handleUpdateButtonPressed.bind(this)
        this.taste=this.taste.bind(this)
    }
    handleName(e){
        this.setState({
            name:e.target.value,
        });
    }
    handleGnere(e){
        this.setState({
            genre:e.target.value,
        });
    }
    handleBase(e){
        this.setState({
            base:e.target.value,
            
        });
    }
    handleUpdateButtonPressed() {
        const requestOptions = {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            genre: this.state.genre,
            code: this.props.roomCode,
          }),
        };
        fetch("/api/update-room", requestOptions).then((response) => {
          if (response.ok) {
            this.setState({
              successMsg: "Room updated successfully!",
            });
          } else {
            this.setState({
              errorMsg: "Error updating room...",
            });
          }
          this.props.updateCallback();
        });
      }
    createR(){


            const requestOptions2 = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              name: this.state.name,
              base: this.state.base,
              taste:this.state.taste,
              genre:this.state.genre
            }),
          };
          fetch("/api/create-room", requestOptions2).then((response) => response.json())
          .then((data) => this.props.history.push("/room/" + data.code));

        }
        taste(){
          const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              taste: this.state.base,
            }),
          }
            fetch("/spotify/taste", requestOptions).then(response=>response.json()).then((data)=>this.setState({taste:data}))
        }

    renderCreate(){
        return(
        <Grid container spacing={1}>
        <Image
            src="https://i.ibb.co/ZdR6TnF/createroom2.png"
            />
        <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} align="center">
                <Typography component={"h4"} variant="h4">Create A Place</Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl>
                    <TextField required={true} label="Name" onChange={this.handleName}></TextField>
                </FormControl>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl>
                    <TextField required={true} label="Base Playlist" onChange={this.handleBase} sx={{"& label": {color: "primary.main"}}}></TextField>
                </FormControl>
            </Grid>
            <Grid item xs={12} align="center">
                <Select label="Genre"value={this.state.genre} onChange={this.handleGnere} >
                    <MenuItem value={"pop rap"}>Pop Rap</MenuItem>
                    <MenuItem value={"pop"}>Pop</MenuItem>
                    <MenuItem value={"edm"}>Edm</MenuItem>
                    <MenuItem value={"electro house"}>Electro House</MenuItem>
                    <MenuItem value={"dance pop"}>Dance Pop</MenuItem>
                    <MenuItem value={"none"}>None</MenuItem>


                </Select>
            </Grid>
            <Grid item xs={12} align="center">
                <Button
            color="primary"
            variant="contained"
            onClick={this.createR}
        >
            Create A Place
                </Button>
            </Grid>
            <Grid item xs={12} align="center">
                <Button
            color="primary"
            variant="contained"
            onClick={this.taste}
        >
            Send Your Taste
                </Button>
            </Grid>
            <Grid item xs={12} align="center">
                <Button color="secondary" variant="contained" to="/" component={Link}>
            Back
                </Button>
            </Grid>
            
        </Grid>
        </Grid>
        )
    }
    renderUpdate(){
        return(
            <Grid container spacing={1}>
                        <Image
          src="https://i.ibb.co/ZdR6TnF/createroom2.png"
                />

            <Grid item xs={12} align="center">
                <Typography component={"h4"} variant="h4">Update The Place</Typography>
                </Grid>
            <Grid item xs={12} align="center">
                <Select label="Genre"value={this.state.genre} onChange={this.handleGnere} >
                    <MenuItem value={"pop rap"}>Pop Rap</MenuItem>
                    <MenuItem value={"pop"}>Pop</MenuItem>
                    <MenuItem value={"edm"}>Edm</MenuItem>
                    <MenuItem value={"electro house"}>Electro House</MenuItem>
                    <MenuItem value={"dance pop"}>Dance Pop</MenuItem>
                    <MenuItem value={"none"}>None</MenuItem>


                </Select>
            </Grid>
            <Grid item xs={12} align="center">
                <Button
            color="primary"
            variant="contained"
            onClick={this.handleUpdateButtonPressed}
        >
            Update A Place
                </Button>
            </Grid>
            </Grid>

        )
    }
    

    render(){
        return (
        <ThemeProvider theme={theme}>
            <CssBaseline/>
            
            
            {this.props.update
          ? this.renderUpdate()
          : this.renderCreate ()}
  
        </ThemeProvider>
            
    )
    }
}
