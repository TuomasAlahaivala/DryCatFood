const TableBody = ({ tableData, columns }) => {
 return (
  <tbody>
   {tableData.length > 0 && tableData.map((data) => {
    return (
     <tr key={data.id}>
      {columns.map(({ accessor }) => {
       const tData = data[accessor] ? data[accessor] : "——";
       console.log(data)
       if (accessor == "title") {
        return <td key={accessor}><a href={data['Product URL']}>{tData}></a></td>;
       }

       return <td key={accessor}>{tData}</td>;
      })}
     </tr>
    );
   })}
  </tbody>
 );
};

export default TableBody;