import React, { Fragment, useState, useEffect } from "react";
import { Redirect } from "react-router-dom";
import {
  getMyFollowers,
  getMyFriendRequests,
  getMyFriends
} from "../../ApiFetchers/getters/Axios";
import ImgUpload from "./ImgUpload";
import NewPostForm from "./NewPostForm";
import {
  Label,
  Menu,
  Dropdown,
  List,
  Button,
  Form,
  Modal,
  ListContent,
  Select,
  Segment
} from "semantic-ui-react";

var username = "dash";
const avatarOptions = [
  {
    key: "myPosts",
    text: "My Channel",
    value: "myPosts",
    icon: "address book outline"
  },
  {
    key: "editProfile",
    text: "Edit Profile",
    value: "editProfile",
    icon: "edit"
  },
  {
    key: "gitActivities",
    text: "Git Activities",
    value: "gitActivities",
    icon: "github"
  },
  {
    key: "signOut",
    text: "Sign Out",
    value: "signOut",
    icon: "delete"
  }
];

const TopBar = () => {
  const [activeItem, setActiveItem] = useState("Followers");
  const [followersLoading, setFollowersLoading] = useState(true);
  const [followers, setFollowers] = useState([]);
  const [friendRequestsLoading, setFriendRequestsLoading] = useState(true);
  const [friendRequests, setFriendRequests] = useState([]);
  const [friendsLoading, setFriendsLoading] = useState(true);
  const [friends, setFriends] = useState([]);
  const [redir, setRedir] = useState(null);
  const handleChange = (e, value) => {
    e.preventDefault();
    setActiveItem(value);
    console.log(value);
  };
  const handleSpecialRoutes = (e, { value }) => {
    e.preventDefault();
    setRedir(value);
  };
  const handleRedir = () => {
    if (redir != null && redir.length > 2) {
      return <Redirect to={redir} />;
    }
  };
  useEffect(() => {
    const followersList = async () => {
      setFollowersLoading(true);
      try {
        let followersFetcher = await getMyFollowers(1); //get data from api's url
        setFollowers(followersFetcher.data);
      } catch (error) {
        console.log(error);
      }
      setFollowersLoading(false);
    }; //fetch followers
    const friendsList = async () => {
      setFriendsLoading(true);
      try {
        let friendsFetcher = await getMyFriends(1); //get data from api's url
        setFriends(friendsFetcher.data);
      } catch (error) {
        console.log(error);
      }
      setFriendsLoading(false);
    }; //fetch friends
    followersList();
    friendsList();
  }, []);

  return (
    <Fragment>
      {handleRedir()}
      <Menu>
        <Menu.Item>
          <a href="/">
            <img
              style={{ height: "45px" }}
              src="https://firebasestorage.googleapis.com/v0/b/book-buddies-d4ba1.appspot.com/o/pepsi.png?alt=media&token=a64adec5-cbb2-475a-9ae4-66f58dfc1bd5"
              alt="Homepage"
            />
          </a>
        </Menu.Item>
        <Modal
          trigger={
            <Menu.Item
              name="Followers"
              active={activeItem === "Followers"}
              onClick={e => handleChange(e, "Followers")}
            >
              Followers
              <Label color="teal">x</Label>
            </Menu.Item>
          }
        >
          <Modal.Header>Current Followers</Modal.Header>
          <Modal.Content>
            <Modal.Description>
              {followersLoading ? (
                <List.Item>
                  <List.Content>
                    <List.Description>Loading ...</List.Description>
                  </List.Content>
                </List.Item>
              ) : (
                <List relaxed>
                  {followers.map(item => (
                    <List.Item key={item.id}>
                      <List.Header>{item.follower}</List.Header>
                      <ListContent flaoted="right">
                        <Button>Accept</Button>
                        <Button>Reject</Button>
                      </ListContent>
                    </List.Item>
                  ))}
                </List>
              )}
            </Modal.Description>
          </Modal.Content>
        </Modal>
        <Modal
          trigger={
            <Menu.Item
              name="Friends"
              active={activeItem === "Friends"}
              onClick={e => handleChange(e, "Friends")}
            >
              Friends
              <Label color="teal">y</Label>
            </Menu.Item>
          }
        >
          <Modal.Header>Current Friends</Modal.Header>
          <Modal.Content>
            <Modal.Description>
              {friendsLoading ? (
                <List.Item>
                  <List.Content>
                    <List.Description>Loading ...</List.Description>
                  </List.Content>
                </List.Item>
              ) : (
                <List relaxed divided>
                  {friends.map(item => (
                    <List.Item key={item.id}>
                      <ListContent>
                        <List.Header as="a">{item.id}</List.Header>
                        <List.Content floated="right">
                          <Button>Unfriend</Button>
                        </List.Content>
                      </ListContent>
                    </List.Item>
                  ))}
                </List>
              )}
            </Modal.Description>
          </Modal.Content>
        </Modal>
        <Modal
          trigger={
            <Menu.Item
              name="Notifications"
              active={activeItem === "Notifications"}
              onClick={e => handleChange(e, "Notifications")}
            >
              Out-Going Requests
              <Label color="teal">z</Label>
            </Menu.Item>
          }
        >
          <Modal.Header>Out Going Requests</Modal.Header>
          <Modal.Content>
            <Modal.Description>
              <p>Notifications</p>
            </Modal.Description>
          </Modal.Content>
        </Modal>
        <Menu.Menu position="right">
          <Modal
            trigger={
              <Menu.Item name="AddPhoto">
                Add Photo
                <Label>*</Label>
              </Menu.Item>
            }
          >
            <Modal.Header>Upload Your Photo</Modal.Header>
            <Modal.Content>
              <ImgUpload />
            </Modal.Content>
          </Modal>
          <Modal
            trigger={
              <Menu.Item name="NewPosts">
                New Post
                <Label>+</Label>
              </Menu.Item>
            }
          >
            <Modal.Header>Create Post</Modal.Header>
            <Modal.Content>
              <NewPostForm />
            </Modal.Content>
          </Modal>
          <div style={{ textAlign: "center", marginTop: "20px" }}>
            <Dropdown
              text={username}
              icon="user"
              size="small"
              floating
              button
              className="icon"
            >
              <Dropdown.Menu>
                {avatarOptions.map(option => (
                  <Dropdown.Item
                    key={option.value}
                    {...option}
                    onClick={handleSpecialRoutes}
                  />
                ))}
              </Dropdown.Menu>
            </Dropdown>
          </div>
        </Menu.Menu>
      </Menu>
    </Fragment>
  );
};

export default TopBar;
