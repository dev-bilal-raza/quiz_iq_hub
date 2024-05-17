import React from 'react'
import { logoutUser } from '@/api-actions/quizApiActions'
import Button from '@/components/layout/Button'
import { useAppDispatch } from '@/app/redux/hooks'
import { logout } from '@/app/redux/features/user/userSlice'
import { useRouter } from 'next/navigation'

const Logout = ({ user_id }: {
  user_id: number
}) => {
  const dispatch = useAppDispatch();
  const router = useRouter()

  const signout = async () => {
    const response = await logoutUser(user_id);
    if (response.ok) {
      console.log(await response.json());
      dispatch(logout());
      router.push("/");
    }
  }
  return (
    <div>
      <Button ButtonType='button' isDeleted={true} onClick={signout}>
        Logout
      </Button>
    </div>
  )
}

export default Logout