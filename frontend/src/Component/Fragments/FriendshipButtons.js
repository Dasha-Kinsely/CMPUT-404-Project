import React, { Fragment, useState, useEffect } from "react";
import {
  getMyFriendRequests,
  getMyFriends,
} from "../../ApiFetchers/getters/Axios";
import { iAccept, iReject } from "../../ApiFetchers/putters/Axios";
import { SliceLocalID } from "../../ClassSupport/APICalls/SliceLocalID";
import {
  Label,
  Menu,
  List,
  Button,
  Modal,
  ListContent,
} from "semantic-ui-react";

var localID = SliceLocalID();
const FriendshipButtons = () => {
  const localToken = localStorage.getItem("currentToken");
  //Rendering Followers
  const [followersLoading, setFollowersLoading] = useState(true);
  const [followersError, setFollowersError] = useState(false);
  const [followers, setFollowers] = useState([]);
  //Rendering Friends
  const [friendsLoading, setFriendsLoading] = useState(true);
  const [friendsError, setFriendsError] = useState(false);
  const [friends, setFriends] = useState([]);
  const handleChange = (e, value) => {
    e.preventDefault();
    //Reinitialize Clientside States
    setFollowers((followers) => []);
    setFriends((friends) => []);
    //Refresh and Fetch from Server
    switch (value) {
      case "Notifications":
        const followersList = async () => {
          setFollowersError(false);
          setFollowersLoading(true);
          try {
            if (localID !== undefined) {
              let friendRequestsFetcher = await getMyFriendRequests(
                localID,
                localToken
              ); //get data from api's url
              let resArray = friendRequestsFetcher.data.authors;
              let loopdex = 0;
              for (let a in resArray) {
                setFollowers((followers) => [
                  ...followers,
                  { index: [loopdex], value: resArray[a] },
                ]);
                loopdex += 1;
              }
              loopdex = 0;
            }
          } catch (error) {
            setFollowersError(true);
          }
          setFollowersLoading(false);
        };
        followersList();
        break;
      case "Friends":
        const friendsList = async () => {
          setFriendsLoading(true);
          setFriendsError(false);
          try {
            if (localID !== undefined) {
              let friendsFetcher = await getMyFriends(localID, localToken); //get data from api's url
              let resArray = friendsFetcher.data.authors;
              let loopdex = 0;
              for (let a in resArray) {
                setFriends((friends) => [
                  ...friends,
                  { index: [loopdex], value: resArray[a] },
                ]);
                loopdex += 1;
              }
              loopdex = 0;
            }
          } catch (error) {
            setFriendsError(true);
          }
          setFriendsLoading(false);
        }; //fetch friends
        friendsList();
        break;
      default:
        return null;
    }
  };

  const accepted = async (e, v) => {
    e.preventDefault();
    let heading = { Authorization: `Token ${localToken}` };
    let res = await iAccept(v.slice(-36), heading);
  };

  const rejected = async (e, v) => {
    e.preventDefault();
    let heading = { Authorization: `Token ${localToken}` };
    let res = await iReject(v.slice(-36), heading);
  };

  const unFriended = async (e, v) => {
    e.preventDefault();
    console.log(v);
    let heading = { Authorization: `Token ${localToken}` };
    //let res = await
  };
  return (
    <Fragment>
      <Modal
        trigger={
          <Menu.Item
            onClick={(e) => {
              handleChange(e, "Notifications");
            }}
          >
            Followers
            <Label color="teal">x</Label>
          </Menu.Item>
        }
      >
        <Modal.Header>Current Followers</Modal.Header>
        <Modal.Content>
          <Modal.Description>
            {followersError && (
              <List.Item>
                <List.Content>
                  <List.Description>Something went wrong ...</List.Description>
                </List.Content>
              </List.Item>
            )}
            {followersLoading ? (
              <List.Item>
                <List.Content>
                  <List.Description>Loading ...</List.Description>
                </List.Content>
              </List.Item>
            ) : (
              <List relaxed>
                {followers !== undefined ? (
                  followers.map((i) => (
                    <List.Item key={i.index}>
                      <List.Header>{i.value}</List.Header>
                      <ListContent floated="right">
                        <Button
                          onClick={(e) => {
                            accepted(e, i.value);
                          }}
                        >
                          Accept
                        </Button>
                        <Button
                          onClick={(e) => {
                            rejected(e, i.value);
                          }}
                        >
                          Reject
                        </Button>
                      </ListContent>
                    </List.Item>
                  ))
                ) : (
                  <List.Item>
                    <List.Description>
                      Something is Not Right...
                    </List.Description>
                  </List.Item>
                )}
              </List>
            )}
          </Modal.Description>
        </Modal.Content>
      </Modal>
      <Modal
        trigger={
          <Menu.Item
            onClick={(e) => {
              handleChange(e, "Friends");
            }}
          >
            Friends
            <Label color="teal">y</Label>
          </Menu.Item>
        }
      >
        <Modal.Header>Current Friends</Modal.Header>
        <Modal.Content>
          <Modal.Description>
            {friendsError && (
              <List.Item>
                <List.Content>
                  <List.Description>Something went wrong ...</List.Description>
                </List.Content>
              </List.Item>
            )}
            {friendsLoading ? (
              <List.Item>
                <List.Content>
                  <List.Description>Loading ...</List.Description>
                </List.Content>
              </List.Item>
            ) : (
              <List relaxed>
                {friends !== undefined ? (
                  friends.map((item) => (
                    <List.Item key={item.index}>
                      <ListContent>
                        <List.Header as="a">{item.value}</List.Header>
                        <List.Content floated="right">
                          <Button
                            onClick={(e) => {
                              unFriended(e, item.value);
                            }}
                          >
                            Unfriend
                          </Button>
                        </List.Content>
                      </ListContent>
                    </List.Item>
                  ))
                ) : (
                  <List.Item>
                    <List.Description>
                      Something is Not Right...
                    </List.Description>
                  </List.Item>
                )}
              </List>
            )}
          </Modal.Description>
        </Modal.Content>
      </Modal>
    </Fragment>
  );
};

export default FriendshipButtons;