import React, { Fragment, useState, useEffect } from "react";
import {
  getMyFollowers,
  getMyFriendRequests,
  getMyFriends
} from "../../ApiFetchers/getters/usersAxios";
import AvatarSelector from "./AvatarSelector";
import ImgUpload from "./ImgUpload";
import NewPostForm from "../Fragments/NewPostForm";
import { Label, Menu, Image, List, Button, Modal } from "semantic-ui-react";

const TopBar = () => {
  const [activeItem, setActiveItem] = useState("Followers");
  const [visability, setVisability] = useState(false);
  const [followersLoading, setFollowersLoading] = useState(true);
  const [followers, setFollowers] = useState([]);
  const [friendRequestsLoading, setFriendRequestsLoading] = useState(true);
  const [friendRequests, setFriendRequests] = useState([]);
  const [friendsLoading, setFriendsLoading] = useState(true);
  const [friends, setFriends] = useState([]);
  const handleChange = (e, value) => {
    e.preventDefault();
    setActiveItem(value);
    console.log(value);
  };
  const handleImageClick = e => {
    e.preventDefault();
    if (visability === true) {
      setVisability(false);
    } else {
      setVisability(true);
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
                    <List.Item>
                      <List.Header>{item.follower}</List.Header>
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
                <List relaxed>
                  {friends.map(item => (
                    <List.Item>
                      <List.Header>{item.id}</List.Header>
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
          <Button.Group>
            <Button onClick={e => handleImageClick(e)}>
              <Image
                avatar
                size="tiny"
                src="https://firebasestorage.googleapis.com/v0/b/book-buddies-d4ba1.appspot.com/o/author.png?alt=media&token=84d333c4-f58c-4223-a454-d94a9d6a4b0f"
              />
              <AvatarSelector />
            </Button>
          </Button.Group>
        </Menu.Menu>
      </Menu>
    </Fragment>
  );
};

export default TopBar;
